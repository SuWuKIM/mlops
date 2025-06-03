import bentoml
import mlflow
from omegaconf import DictConfig


def register_mlflow_to_bentoml(cfg: DictConfig):
    model_name = cfg.serving.model_name
    mlflow_model_uri = cfg.mlflow.model_uri
    model_labels = cfg.serving.labels
    mlflow_uri = cfg.mlflow.tracking_uri

    mlflow.set_tracking_uri(mlflow_uri)
    bentoml.mlflow.import_model(model_name, mlflow_model_uri, labels=model_labels)

    return bentoml.mlflow.load_model(f"{model_name}:latest")
