from airflow.decorators import dag
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
import os

from pipeline.template import TrainerDagBuilder


class DiseaseTrainerDagBuilder(TrainerDagBuilder):
    def __init__(self):
        super().__init__("disease")

    def create_dag(self):
        params = {"env": "dev", "PAT": ""}

        @dag(**self.dag_args, params=params, schedule=None)
        def def_dag():
            dataset = self.fetch_dataset_task()
            code = self.clone_code_task()
            trainer = self.train_task()
            [dataset(), code()] >> trainer

        return def_dag()


tmp_dir = "/tmp_run"
host_tmp_dir = os.path.join(os.getcwd(), "tmp_run")

docker_task = DockerOperator(
    task_id='train-disease-in-docker',
    image='trainer:3.12',
    command='python /app/train_disease.py',
    mount_tmp_dir=False,
    mounts=[
        Mount(
            source=host_tmp_dir,
            target='/app',
            type='bind'
        )
    ],
    working_dir='/app',
    network_mode='bridge',
    auto_remove=True
)

dag = DiseaseTrainerDagBuilder().create_dag()
