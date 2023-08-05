# Copyright 2022-2023 Qiskit on IQM developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Fake backend for simulating IQM quantum computers.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Optional, Union

from iqm_client import QuantumArchitectureSpecification
from qiskit import QuantumCircuit
from qiskit.providers import JobV1, Options
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_aer.noise.errors import depolarizing_error, thermal_relaxation_error

from qiskit_iqm.iqm_backend import IQM_TO_QISKIT_GATE_NAME, IQMBackendBase


@dataclass
class IQMErrorProfile:
    """Collection of various properties of an IQM QPU to be used for constructing error model.

    Args:
        t1s: :math:`T_1` times (in ns) for each qubit of the chip, corresponding key is the physical qubit name.
        t2s: :math:`T_2` times (in ns) for each qubit of the chip, corresponding key is the physical qubit name.
        single_qubit_gate_depolarizing_error_parameters: Depolarizing error parameters for single-qubit gates of each
            qubit. Using the values in the depolarizing channel, concatenated with a thermal relaxation channel,
            lead to average gate fidelities that would be determined by benchmarking.
        two_qubit_gate_depolarizing_error_parameters: Depolarizing error parameters for two-qubit gates of each
            connection. Using the values in the depolarizing channel, concatenated with a thermal relaxation channel,
            lead to average gate fidelities that would be determined by benchmarking.
        single_qubit_gate_durations: Gate duration (in ns) for each single-qubit gate
        two_qubit_gate_durations: Gate duration (in ns) for each two-qubit gate.
        id_: Identifier of the chip sample. Defaults to None.

    Example:
        .. code-block::

            IQMErrorProfile(
                t1s={"QB1": 10000.0, "QB2": 12000.0, "QB3": 14000.0},
                t2s={"QB1": 10000.0, "QB2": 12000.0, "QB3": 13000.0},
                single_qubit_gate_depolarizing_error_parameters={"r": {"QB1": 0.0005, "QB2": 0.0004, "QB3": 0.0010}},
                two_qubit_gate_depolarizing_error_parameters={"cz": {("QB1", "QB2"): 0.08, ("QB2", "QB3"): 0.03}},
                single_qubit_gate_durations={"r": 50.},
                two_qubit_gate_durations={"cz": 100.},
                id_="threequbit-example_sample"
            )
    """

    t1s: dict[str, float]
    t2s: dict[str, float]
    single_qubit_gate_depolarizing_error_parameters: dict[str, dict[str, float]]
    two_qubit_gate_depolarizing_error_parameters: dict[str, dict[tuple[str, str], float]]
    single_qubit_gate_durations: dict[str, float]
    two_qubit_gate_durations: dict[str, float]
    id_: Union[str, None] = None


class IQMFakeBackend(IQMBackendBase):
    """Fake backend that mimics the behaviour of IQM quantum computers. Can be used to perform noisy gate-level
    simulations of quantum circuit execution on IQM hardware.

    A fake backend contains information about a specific IQM system, such as the quantum architecture (number of qubits,
    connectivity), the native gate set, and a noise model based on system parameters such as relaxation (:math:`T_1`)
    and decoherence (:math:`T_2`) times and gate infidelities.

    Args:
        architecture: Description of the quantum architecture associated with the backend instance.
        chip_sample: Describes the characteristics of a specific chip sample.
    """

    def __init__(self, architecture: QuantumArchitectureSpecification, error_profile: IQMErrorProfile, **kwargs):
        super().__init__(architecture, **kwargs)

        self._validate_architecture_and_error_profile(architecture, error_profile)
        self.__architecture, self.__error_profile = architecture, error_profile

        self.noise_model = self._create_noise_model(architecture, error_profile)

    @property
    def error_profile(self) -> IQMErrorProfile:
        """Error profile of this instance of IQM fake backend"""
        return deepcopy(self.__error_profile)

    @error_profile.setter
    def error_profile(self, value: IQMErrorProfile) -> None:
        """"""
        raise NotImplementedError(
            "Setting error profile of existing fake backend is not allowed. "
            "You may consider using the method .copy_with_error_profile."
        )

    def copy_with_error_profile(self, new_error_profile: IQMErrorProfile) -> IQMFakeBackend:
        """Return another instance of IQMFakeBackend, which has the same quantum architecture but a different error
        profile."""
        return self.__class__(self.__architecture, new_error_profile)

    @staticmethod
    def _validate_architecture_and_error_profile(
        architecture: QuantumArchitectureSpecification, error_profile: IQMErrorProfile
    ) -> None:
        """Verifies that the parameters of the chip sample match the constraints of its IQMQuantumArchitecture.

        Raises:
            ValueError: when length of `t1s` and number of qubits do not match.
            ValueError: when length of `t2s` and number of qubits do not match.
            ValueError: when length of `one_qubit_gate` parameter lists and number of qubits do not match.
            ValueError: when length of `two_qubit_gate` parameter lists and number of couplings do not match.
            ValueError: when gates in gate parameter lists are not supported by the quantum architecture.
        """
        num_qubits = len(architecture.qubits)
        # Check that T1 list has one element for each qubit
        if len(error_profile.t1s) != num_qubits:
            raise ValueError(
                f"Length of t1s ({len(error_profile.t1s)}) and number of qubits ({num_qubits}) should match."
            )

        # Check that T2 list has one element for each qubit
        if len(error_profile.t2s) != num_qubits:
            raise ValueError(
                f"Length of t2s ({len(error_profile.t2s)}) and number of qubits ({num_qubits}) should match."
            )

        property_dict: dict[str, dict[Any, float]]
        # Check that one-qubit gate parameter qubits match those of the architecture
        for property_name, property_dict in [
            ("depolarizing rates", error_profile.single_qubit_gate_depolarizing_error_parameters),
        ]:
            gate_dict: dict[Any, float]
            for gate, gate_dict in property_dict.items():
                if set(gate_dict.keys()) != set(architecture.qubits):
                    raise ValueError(
                        (
                            f"The qubits specified for one-qubit gate {property_name} ({set(gate_dict.keys())}) "
                            f"don't match the qubits of the quantum architecture "
                            f"`{architecture.name}` ({architecture.qubits})."
                        )
                    )

        # Check that two-qubit gate parameter couplings match those of the architecture
        for property_name, property_dict in [
            ("depolarizing error parameters", error_profile.two_qubit_gate_depolarizing_error_parameters),
        ]:
            for gate, gate_dict in property_dict.items():
                if set(gate_dict.keys()) != set(tuple(item) for item in architecture.qubit_connectivity):
                    raise ValueError(
                        (
                            f"The couplings specified for two-qubit gate {property_name} ({set(gate_dict.keys())}) "
                            f"don't match the couplings of the quantum architecture "
                            f"`{architecture.name}` ({architecture.qubit_connectivity})."
                        )
                    )

        # Check that the basis gates of the chip sample match the quantum architecture's
        for property_name, specified_gates in [
            (
                "single qubit gate depolarizing_error_parameters",
                error_profile.single_qubit_gate_depolarizing_error_parameters.keys(),
            ),
            (
                "two qubit gate depolarizing_error_parameters",
                error_profile.two_qubit_gate_depolarizing_error_parameters.keys(),
            ),
            ("durations", (error_profile.single_qubit_gate_durations | error_profile.two_qubit_gate_durations).keys()),
        ]:
            for gate in specified_gates:
                if gate not in architecture.operations:
                    raise ValueError(
                        (
                            f"Gate `{gate}` in `gate_{property_name}` "
                            "is not supported by quantum architecture `{self.quantum_architecture.id_}`. "
                            f"Valid gates: {architecture.operations}"
                        )
                    )

    def _create_noise_model(
        self, architecture: QuantumArchitectureSpecification, error_profile: IQMErrorProfile
    ) -> NoiseModel:
        """
        Builds a noise model from the attributes.
        """
        noise_model = NoiseModel(basis_gates=["r", "cz"])

        # Add single-qubit gate errors to noise model
        for gate in error_profile.single_qubit_gate_depolarizing_error_parameters.keys():
            for qb in architecture.qubits:
                thermal_relaxation_channel = thermal_relaxation_error(
                    error_profile.t1s[qb], error_profile.t2s[qb], error_profile.single_qubit_gate_durations[gate]
                )
                depolarizing_channel = depolarizing_error(
                    error_profile.single_qubit_gate_depolarizing_error_parameters[gate][qb], 1
                )
                full_error_channel = thermal_relaxation_channel.compose(depolarizing_channel)
                noise_model.add_quantum_error(
                    full_error_channel, IQM_TO_QISKIT_GATE_NAME[gate], [self.qubit_name_to_index(qb)]
                )

        # Add two-qubit gate errors to noise model
        for gate, rates in error_profile.two_qubit_gate_depolarizing_error_parameters.items():
            for (qb1, qb2), rate in rates.items():
                thermal_relaxation_channel = thermal_relaxation_error(
                    error_profile.t1s[qb1],
                    error_profile.t2s[qb1],
                    error_profile.two_qubit_gate_durations[gate],
                ).tensor(
                    thermal_relaxation_error(
                        error_profile.t1s[qb2],
                        error_profile.t2s[qb2],
                        error_profile.two_qubit_gate_durations[gate],
                    )
                )
                depolarizing_channel = depolarizing_error(rate, 2)
                full_error_channel = thermal_relaxation_channel.compose(depolarizing_channel)
                noise_model.add_quantum_error(
                    full_error_channel,
                    IQM_TO_QISKIT_GATE_NAME[gate],
                    [self.qubit_name_to_index(qb1), self.qubit_name_to_index(qb2)],
                )

        return noise_model

    @classmethod
    def _default_options(cls) -> Options:
        return Options(shots=1024, calibration_set_id=None)

    @property
    def max_circuits(self) -> Optional[int]:
        return None

    def run(self, run_input: Union[QuantumCircuit, list[QuantumCircuit]], **options) -> JobV1:
        """
        Run `run_input` on the fake backend using a simulator.

        This method runs circuit jobs (an individual or a list of QuantumCircuit
        ) and returns a :class:`~qiskit.providers.JobV1` object.

        It will run the simulation with a noise model of the fake backend (e.g. Adonis).

        Args:
            run_input: One or more quantum circuits to simulate on the backend.
            options: Any kwarg options to pass to the backend.
        Returns:
            The job object representing the run.
        Raises:
            ValueError: If empty list of circuits is provided.
        """
        circuits = [run_input] if isinstance(run_input, QuantumCircuit) else run_input

        if len(circuits) == 0:
            raise ValueError("Empty list of circuits submitted for execution.")

        shots = options.get("shots", self.options.shots)

        # Create noisy simulator backend and run circuits
        sim_noise = AerSimulator(noise_model=self.noise_model)
        job = sim_noise.run(circuits, shots=shots)

        return job
