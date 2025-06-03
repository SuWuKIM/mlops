import bentoml

from bentos.classifier import BentoMLFlowClassifier
from bentos.register import register_mlflow_to_bentoml
from utils.configs import load_bento_config

cfg = load_bento_config(__file__)
model = register_mlflow_to_bentoml(cfg)


@bentoml.service(resources=cfg.service.resources, traffic=cfg.service.traffic)
class BentoDiseaseClassifier(BentoMLFlowClassifier):
    def __init__(self):
        super().__init__(model)
