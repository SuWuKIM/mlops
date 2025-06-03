from airflow.decorators import dag

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


dag = DiseaseTrainerDagBuilder().create_dag()
