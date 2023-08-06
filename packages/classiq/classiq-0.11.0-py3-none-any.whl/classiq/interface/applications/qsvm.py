from collections.abc import Sequence
from enum import Enum, auto
from typing import Any, Iterable as IterableType, List, Optional, Union

import numpy as np
import pydantic
from numpy.typing import ArrayLike

from classiq.interface.executor.execution_preferences import ExecutionPreferences

DataList = List[List[float]]
LabelsInt = List[int]


def listify(obj: Union[IterableType, ArrayLike]) -> list:
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, Sequence) and obj and isinstance(obj[0], np.ndarray):
        return np.array(obj).tolist()
    elif isinstance(obj, list):
        return obj
    else:
        return list(obj)  # type: ignore[arg-type]


class QSVMPreferences(pydantic.BaseModel):
    execution_preferences: ExecutionPreferences
    l2_norm_regularization_factor: float = 0.001


class QSVMFeatureMapEntanglement(str, Enum):
    FULL = "full"
    LINEAR = "linear"
    CIRCULAR = "circular"
    SCA = "sca"
    PAIRWISE = "pairwise"


class QSVMFeatureMapDimensional(pydantic.BaseModel):
    feature_dimension: Optional[int] = None

    class Config:
        extra = "forbid"


VALID_PAULI_LETTERS = ("I", "X", "Y", "Z")


class QSVMFeatureMapPauli(QSVMFeatureMapDimensional):
    reps: int = 2
    entanglement: QSVMFeatureMapEntanglement = QSVMFeatureMapEntanglement.LINEAR
    alpha: float = 2.0
    paulis: List[str] = ["Z", "ZZ"]
    parameter_prefix: str = "x"
    name: str = "PauliFeatureMap"

    @pydantic.validator("paulis", pre=True)
    def set_paulis(cls, paulis):
        # iterate every letter in every string in the list of paulis
        for s in paulis:
            if not all(map(VALID_PAULI_LETTERS.__contains__, s.upper())):
                raise ValueError(
                    f'Invalid pauli string given: "{s}". Expecting a combination of {VALID_PAULI_LETTERS}'
                )
        return list(map(str.upper, paulis))


class QSVMFeatureMapBlochSphere(QSVMFeatureMapDimensional):
    pass


FeatureMapType = Union[QSVMFeatureMapBlochSphere, QSVMFeatureMapPauli]

Point = List[float]
Label = int  # 0 or 1


class QSVMInternalState(pydantic.BaseModel):
    alphas: List[float]
    bias: float
    support_vectors: List[Point]
    support_vectors_labels: List[Label]

    @pydantic.validator("alphas", pre=True)
    def set_alphas(cls, alphas):
        return listify(alphas)

    @pydantic.validator("support_vectors", pre=True)
    def set_support_vectors(cls, support_vectors):
        return listify(support_vectors)

    @pydantic.validator("support_vectors_labels", pre=True)
    def set_support_vectors_labels(cls, support_vectors_labels):
        return listify(support_vectors_labels)


class QSVMData(pydantic.BaseModel):
    data: DataList
    labels: Optional[LabelsInt] = None
    feature_map: FeatureMapType
    internal_state: Optional[QSVMInternalState] = None
    preferences: QSVMPreferences

    class Config:
        smart_union = True

    @pydantic.validator("data", pre=True)
    def set_data(cls, data):
        return listify(data)

    @pydantic.validator("labels", pre=True)
    def set_labels(cls, labels):
        if labels is None:
            return None
        else:
            return listify(labels)


class QSVMResultStatus(Enum):
    SUCCESS = auto()
    FAILED = auto()


class QSVMResult(pydantic.BaseModel):
    status: QSVMResultStatus
    details: Optional[Any] = None  # anything that's convertible to string
    result: dict = pydantic.Field(default_factory=dict)
