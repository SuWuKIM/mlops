# 벤또 서빙 (모듈 방식)
- bentoml serve models.disease_classifier.make_bento:BentoDiseaseClassifier --port 3000 --working-dir .

# BentoML 주의 사항
- 타입 힌트에 Typing 활용
  - def predict(...) -> Dict[str, any]  (X)
  - def predict(...) -> Dict[str, Any]  (O)

- 설정 yaml 문자열 값 주의 (특수 문자 있는 경우 따옴표 처리)
  - "runs:/d5899ca505ee411fa20ecd8f3197cae3/disease_rf_model"  

- bentoml import 사용 시 set_tracking_url은 mlflow 패키지 수행 (bentoml.mlflow X)
```
import bentoml
import mlflow

mlflow.set_tracking_uri(mlflow_uri)
bentoml.mlflow.import_model(model_name, mlflow_model_uri, labels=model_labels)
```