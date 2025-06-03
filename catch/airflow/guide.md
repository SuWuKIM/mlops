# NOTE
- 컴포즈 간 네임스페이스 구분 위해 -p 옵션 사용


# airflow compose 파일
- curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.1/docker-compose.yaml'

# .env 파일 생성
- uid, gid, etc ...

# airflow 컴포즈 최초 실행
- docker compose -p airflow up airflow-init

# 실제 컴포즈 시행전 .env 반영사항 체크
- docker compose config

# airflow 시작 (build 없이)
- docker compose -p airflow up -d

# airflow 시작 (Dockerfile 변경 빌드)
- docker compose up --build -d

# airflow 내리기
- docker compose -p airflow down

# dag force reload (in airflow-worker container)
- airflow dags reserialize

# NOTE
- @dag이 최종 정의 파일에 존재해야 airflow 인식함
   - ex. train_imdb.py 파일에 @dag 존재 해야 함

# requirement.trainer.txt
- 모델 훈련 도커 컨테이너에 필요한 파이썬 패키지 추가

# trainer 도커 이미지 빌드 (deprecated: .env등 편의를 위해 컴포즈로)
- docker build -t trainer:3.12 -f Dockerfile.trainer .

# trainer 도커 컴포즈로 빌드 
- docker compose -f docker-compose.trainer.yaml -p trainer up

