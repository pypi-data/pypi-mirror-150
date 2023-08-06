from dataclasses import dataclass
from typing import Optional, Union, cast

from classiq.interface.chemistry.ground_state_problem import GroundStateProblem
from classiq.interface.chemistry.ground_state_result import (
    GroundStateExactResult,
    GroundStateResult,
)
from classiq.interface.executor.execution_preferences import (
    BackendPreferencesTypes,
    ExecutionPreferences,
)
from classiq.interface.executor.hamiltonian_minimization_problem import (
    HamiltonianMinimizationProblem,
)
from classiq.interface.executor.optimizer_preferences import GroundStateOptimizer
from classiq.interface.executor.quantum_instruction_set import QuantumInstructionSet
from classiq.interface.executor.quantum_program import QuantumProgram
from classiq.interface.executor.result import ExecutionStatus
from classiq.interface.generator.result import GeneratedCircuit, QuantumFormat

from classiq import Executor
from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import Asyncify
from classiq._internals.type_validation import validate_type
from classiq.applications.ground_state_problem import generate_hamiltonian_async
from classiq.exceptions import ClassiqError, ClassiqExecutionError


@dataclass
class GroundStateSolver(metaclass=Asyncify):
    ground_state_problem: GroundStateProblem
    ansatz: Union[str, GeneratedCircuit, None] = None
    optimizer_preferences: Optional[GroundStateOptimizer] = None

    async def solve_async(
        self, backend_preferences=BackendPreferencesTypes
    ) -> GroundStateResult:
        operator = await generate_hamiltonian_async(
            gs_problem=self.ground_state_problem
        )
        if self.ansatz is None:
            raise ValueError("ansatz field must be specified")
        if self.optimizer_preferences is None:
            raise ValueError("optimizer_preferences field must be specified")

        # when incorporating OPENQASM3, OPENQASM 3, OPENQASM 3.0, QASM 3.0, this might need updating
        if isinstance(self.ansatz, GeneratedCircuit):
            if QuantumFormat.QASM in self.ansatz.output_format:
                circuit_code = self.ansatz.qasm
        elif isinstance(self.ansatz, str) and "OPENQASM" in self.ansatz:
            circuit_code = self.ansatz
        else:
            raise ValueError(
                "unknown circuit format. Supported circuit formats are: qasm"
            )
        circuit_syntax = QuantumInstructionSet.QASM

        hamiltonian_problem = HamiltonianMinimizationProblem(
            ansatz=QuantumProgram(code=circuit_code, syntax=circuit_syntax),
            hamiltonian=operator,
        )
        execution_preferences = ExecutionPreferences(
            num_shots=self.optimizer_preferences.num_shots,
            backend_preferences=backend_preferences,
            optimizer_preferences=self.optimizer_preferences,
            random_seed=self.optimizer_preferences.random_seed,
        )
        result = await Executor(
            preferences=execution_preferences
        ).execute_hamiltonian_minimization_async(hamiltonian_problem)

        return cast(GroundStateResult, result)

    async def solve_exact_async(self) -> GroundStateExactResult:
        result = await ApiWrapper.call_solve_exact_task(
            problem=self.ground_state_problem
        )

        if result.status != ExecutionStatus.SUCCESS:
            raise ClassiqError(f"solve_exact failed: {result.details}")

        return validate_type(
            obj=result.details,
            expected_type=GroundStateExactResult,
            operation="Exact solution",
            exception_type=ClassiqExecutionError,
        )
