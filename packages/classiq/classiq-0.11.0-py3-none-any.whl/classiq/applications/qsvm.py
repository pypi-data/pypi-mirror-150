from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

from classiq.interface.applications.qsvm import (
    DataList,
    FeatureMapType,
    QSVMData,
    QSVMFeatureMapBlochSphere,
    QSVMFeatureMapPauli,
    QSVMInternalState,
    QSVMPreferences,
    QSVMResultStatus,
)
from classiq.interface.backend.backend_preferences import IBMBackendPreferences
from classiq.interface.executor.execution_preferences import ExecutionPreferences

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import Asyncify
from classiq.applications import numpy_utils
from classiq.exceptions import ClassiqQSVMError, ClassiqValueError

Data = Union[DataList, np.ndarray]
Labels = Union[List[Any], np.ndarray]
FeatureMap = Union[FeatureMapType, str, List[str]]

_DEFAULT_EXECUTION_PREFERENCES = ExecutionPreferences(
    num_shots=1024,
    backend_preferences=IBMBackendPreferences(backend_name="aer_simulator"),
    random_seed=1234,
)


class QSVM(metaclass=Asyncify):
    def __init__(
        self,
        feature_map: FeatureMap,
        train_data: Optional[Data] = None,
        train_labels: Optional[Labels] = None,
        test_data: Optional[Data] = None,
        test_labels: Optional[Labels] = None,
        predict_data: Optional[Data] = None,
        preferences: Optional[QSVMPreferences] = None,
        **preferences_kwargs,
    ):
        self._set_feature_map(feature_map)

        self._train_data = train_data
        self._train_labels = train_labels
        self._test_data = test_data
        self._test_labels = test_labels
        self._predict_data = predict_data
        self._result: dict = {}

        self._set_preferences(preferences, preferences_kwargs)

        labels = numpy_utils.choose_first(self._train_labels, self._test_labels)
        if labels is not None:
            self._generate_label_map(labels)

    def _set_feature_map(self, feature_map: FeatureMap) -> None:
        if isinstance(feature_map, FeatureMapType.__args__):  # type: ignore[attr-defined]
            self._feature_map = feature_map
        elif isinstance(feature_map, str):
            if feature_map == "bloch_sphere":
                self._feature_map = QSVMFeatureMapBlochSphere()
            elif feature_map == "pauli":
                self._feature_map = QSVMFeatureMapPauli()
            else:
                raise ClassiqValueError(
                    'Invalid feature map entered. Please enter either "bloch_sphere" or a list of pauli operators'
                )
        elif isinstance(feature_map, list):
            self._feature_map = QSVMFeatureMapPauli(paulis=feature_map)
        else:
            raise ClassiqValueError(
                'Invalid feature map entered. Please enter either "bloch_sphere" or a list of pauli operators'
            )

    def _set_preferences(
        self, preferences: Optional[QSVMPreferences], preferences_kwargs: dict
    ):
        if preferences is not None:
            self.preferences = preferences
        else:
            if "execution_preferences" not in preferences_kwargs:
                preferences_kwargs[
                    "execution_preferences"
                ] = _DEFAULT_EXECUTION_PREFERENCES

            self.preferences = QSVMPreferences(**preferences_kwargs)

    def _generate_label_map(self, labels: Labels) -> None:
        self._label_to_int_map: Dict[Any, int] = {
            label: index for index, label in enumerate(sorted(set(labels)))
        }
        self._int_to_label_map: Dict[int, Any] = {
            index: label for index, label in enumerate(sorted(set(labels)))
        }

    def _label_to_int(self, labels: Labels) -> List[int]:
        if not hasattr(self, "_label_to_int_map"):
            self._generate_label_map(labels)

        return [self._label_to_int_map[i] for i in labels]

    def _int_to_label(self, ints: List[int]) -> List[Any]:
        if not hasattr(self, "_int_to_label_map"):
            raise ClassiqValueError(
                "Unable to translate int to label without conversion map"
            )

        return [self._int_to_label_map[i] for i in ints]

    async def run_async(
        self,
        train_data: Optional[Data] = None,
        train_labels: Optional[Labels] = None,
        test_data: Optional[Data] = None,
        test_labels: Optional[Labels] = None,
        predict_data: Optional[Data] = None,
        preferences: Optional[QSVMPreferences] = None,
        **preferences_kwargs,
    ) -> dict:
        if preferences or preferences_kwargs:
            self._set_preferences(preferences, preferences_kwargs)

        self._train_data = numpy_utils.choose_first(train_data, self._train_data)
        self._train_labels = numpy_utils.choose_first(train_labels, self._train_labels)
        if numpy_utils.bool_data(self._train_data, self._train_labels):
            await self.train_async()

        self._test_data = numpy_utils.choose_first(test_data, self._test_data)
        self._test_labels = numpy_utils.choose_first(test_labels, self._test_labels)
        if numpy_utils.bool_data(self._test_data, self._test_labels):
            await self.test_async()

        self._predict_data = numpy_utils.choose_first(predict_data, self._predict_data)
        if numpy_utils.bool_data(self._predict_data):
            await self.predict_async()

        return self._result

    async def train_async(
        self, data: Optional[Data] = None, labels: Optional[Labels] = None
    ) -> np.ndarray:
        data = numpy_utils.choose_first(data, self._train_data)
        if not numpy_utils.bool_data(data):
            raise ClassiqValueError("Empty data was supplied")

        labels = numpy_utils.choose_first(labels, self._train_labels)
        if not numpy_utils.bool_data(labels):
            raise ClassiqValueError("Empty labels was supplied")

        result = await ApiWrapper().call_qsvm_train(
            self._prepare_qsvm_data(data, labels)  # type: ignore[arg-type]
        )

        if result.status != QSVMResultStatus.SUCCESS:
            raise ClassiqQSVMError(f"Training failed: {result.details}")

        return self._process_train_result(result.result)

    def _process_train_result(self, result: dict) -> np.ndarray:
        # post-process result
        self.kernel_matrix_training = result["kernel_matrix"] = np.array(
            result["kernel_matrix"]
        )
        self.alphas = result["alphas"] = np.array(result["alphas"])
        self.bias = result["bias"]
        self.support_vectors = result["support_vectors"] = np.array(
            result["support_vectors"]
        )
        self.support_vectors_labels = result["support_vectors_labels"] = np.array(
            result["support_vectors_labels"]
        )
        # store the result
        self._result["train"] = result
        # return the result
        return self.kernel_matrix_training

    async def test_async(
        self, data: Optional[Data] = None, labels: Optional[Labels] = None
    ) -> Tuple[np.ndarray, float]:
        if not self._is_trained:
            raise ClassiqQSVMError("Cannot test QSVM on an un-trained model")

        data = numpy_utils.choose_first(data, self._test_data)
        if not numpy_utils.bool_data(data):
            raise ClassiqValueError("Empty data was supplied")

        labels = numpy_utils.choose_first(labels, self._test_labels)
        if not numpy_utils.bool_data(labels):
            raise ClassiqValueError("Empty labels was supplied")

        result = await ApiWrapper().call_qsvm_test(
            self._prepare_qsvm_data(data, labels)  # type: ignore[arg-type]
        )

        if result.status != QSVMResultStatus.SUCCESS:
            raise ClassiqQSVMError(f"Testing failed: {result.details}")

        return self._process_test_result(result.result)

    def _process_test_result(self, result: dict) -> Tuple[np.ndarray, float]:
        # post-process result
        self.kernel_matrix_test = result["kernel_matrix"] = np.array(
            result["kernel_matrix"]
        )
        self.accuracy = result["accuracy"]
        # store the result
        self._result["test"] = result
        # return the result
        return self.kernel_matrix_test, self.accuracy

    async def predict_async(self, data: Optional[Data] = None) -> Labels:
        if not self._is_trained:
            raise ClassiqQSVMError("Cannot test QSVM on an un-trained model")

        data = numpy_utils.choose_first(data, self._predict_data)
        if not numpy_utils.bool_data(data):
            raise ClassiqValueError("Empty data was supplied")

        result = await ApiWrapper().call_qsvm_predict(self._prepare_qsvm_data(data))  # type: ignore[arg-type]

        if result.status != QSVMResultStatus.SUCCESS:
            raise ClassiqQSVMError(f"Predicting failed: {result.details}")

        return self._process_predict_result(result.result)

    def _process_predict_result(self, result: dict) -> Labels:
        # post-process result
        result["labels"] = np.array(self._int_to_label(result["labels"]))
        # store the result
        self._result["predict"] = result
        # return the result
        return result["labels"]

    def _prepare_qsvm_data(
        self, data: Data, labels: Optional[Labels] = None
    ) -> QSVMData:
        if self._feature_map.feature_dimension is None:
            self._feature_map.feature_dimension = len(data[0])

        if len(data[0]) != self._feature_map.feature_dimension:
            raise ClassiqQSVMError(
                "The shape of the data is incompatible with the feature map"
            )

        if labels is not None:
            return QSVMData(
                data=data,
                labels=self._label_to_int(labels),
                feature_map=self._feature_map,
                internal_state=self._internal_state,
                preferences=self.preferences,
            )
        else:
            return QSVMData(
                data=data,
                feature_map=self._feature_map,
                internal_state=self._internal_state,
                preferences=self.preferences,
            )

    @property
    def _is_trained(self) -> bool:
        return all(
            map(self.__dict__.__contains__, QSVMInternalState.__annotations__.keys())
        )

    @property
    def _internal_state(self) -> Optional[QSVMInternalState]:
        if self._is_trained:
            return QSVMInternalState(
                **{
                    k: getattr(self, k)
                    for k in QSVMInternalState.__annotations__.keys()
                }
            )
        else:
            return None
