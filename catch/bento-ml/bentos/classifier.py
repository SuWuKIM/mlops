from typing import List, Dict, Any

import bentoml
import numpy as np


class BentoMLFlowClassifier:
    def __init__(self, model):
        self.model = model

    @bentoml.api
    def predict(self, input_data: list) -> Dict[str, Any]:
        if not isinstance(input_data, list):
            return {
                "status": "failed",
                "error": f"type mismatch. type got: {type(input_data)}",
            }

        ins = np.array([input_data])
        ins.reshape((-1, 132))
        pred = self.model.predict(ins)
        return {
            "prediction": pred.tolist(),
            "status": "success",
        }

    @bentoml.api
    def predict_batch(self, input_data: List[np.ndarray]) -> Dict[str, Any]:
        return {
            "predictions": [],
            "count": 0,
            "status": "failed",
            "error": "not implemented yet",
        }

    @bentoml.api
    def health(self) -> Dict[str, str]:
        return {
            "status": "healthy",
            "model_tag": str(self.model.tag),
        }

    @bentoml.api
    def model_info(self) -> Dict[str, Any]:
        return {
            "creation_time": self.model.info.creation_time.isoformat(),
            "labels": dict(self.model.info.labels),
            "metadata": (
                dict(self.model.info.metadata) if self.model.info.metadata else {}
            ),
        }
