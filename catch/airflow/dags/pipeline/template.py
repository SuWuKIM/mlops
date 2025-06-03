import os
from abc import abstractmethod

from airflow.decorators import task
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

from tasks.config import load_hydra_config
from tasks.git import git_clone
from tasks.s3 import S3


# TODO
# - tmp_volume run-id 처리 (현재 airflow 모델 훈련 병렬로 처리 불가)
class TrainerDagTemplate:
    def __init__(self, key: str):
        self.key = key
        self.cfg = load_hydra_config()
        self.setup_dataset_dirs()
        self.s3 = self.setup_s3()

    @property
    def model_conf(self):
        return self.cfg[self.key]

    @property
    def code_dir(self):
        return os.path.join(self.cfg.tmp_volume, "code")

    @property
    def dataset_dir(self):
        return os.path.join(self.cfg.tmp_volume, "dataset")

    def get_repo_url(self, params):
        repo = self.model_conf.repo
        pat = params.get("PAT", None)
        if pat and "{pat}" in repo:
            return self.model_conf.repo.format(pat=pat)
        return repo

    def get_clone_branch(self, params):
        branch = params.get("branch", None)
        return branch if branch else self.model_conf.branch

    def setup_dataset_dirs(self):
        os.makedirs(self.dataset_dir, exist_ok=True)

    def setup_s3(self):
        s3 = self.model_conf.s3
        return S3(s3.endpoint, s3.access_key, s3.secret_key, self.dataset_dir)

    def fetch_dataset_task(self):
        @task(task_id=f"fetch-{self.key}-dataset")
        def task_func():
            self.fetch_dataset()
            print("fetch dataset success")

        return task_func

    def clone_code_task(self):
        @task(task_id=f"clone-{self.key}-code")
        def task_func(**context):
            self.clone_code(**context)
            print("clone code success")

        return task_func

    def train_task(self):
        cmd = f"python /tmp_run/code/{self.model_conf.entry}"
        trainer = DockerOperator(
            task_id=f"train-{self.key}-in-docker",
            command=cmd,
            image=self.model_conf.trainer_image,
            network_mode="host",  # localhost 바로 접근 가능
            auto_remove="success",
            docker_url="unix://var/run/docker.sock",
            mount_tmp_dir=False,
            mounts=[
                Mount(source=self.cfg.tmp_volume_host, target="/tmp_run", type="bind")
            ],
        )
        return trainer

    @abstractmethod
    def fetch_dataset(self):
        raise NotImplementedError()

    @abstractmethod
    def clone_code(self, **context):
        raise NotImplementedError()


class TrainerDagBuilder(TrainerDagTemplate):
    def __init__(self, key: str):
        super().__init__(key)

    def fetch_dataset(self):
        s3 = self.model_conf.s3
        for key in s3.dataset_keys:
            self.s3.down(s3.bucket, key)

    def clone_code(self, **context):
        params = context.get("params", {})
        branch = self.get_clone_branch(params)
        repo = self.get_repo_url(params)
        git_clone(repo, branch, self.code_dir)

    @property
    def dag_args(self):
        return {
            "dag_id": f"train-{self.key}",
            "tags": self.model_conf.tags.split(","),
            "description": self.model_conf.desc,
        }

    @abstractmethod
    def create_dag(self):
        raise NotImplementedError()
