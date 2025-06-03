from airflow.decorators import dag

from pipeline.template import TrainerDagBuilder


class IMDBTrainerDagBuilder(TrainerDagBuilder):
    def __init__(self):
        super().__init__("imdb")

    def create_dag(self):
        params = {"env": "dev", "PAT": ""}

        @dag(**self.dag_args, params=params, schedule=None)
        def def_dag():
            dataset = self.fetch_dataset_task()
            code = self.clone_code_task()
            trainer = self.train_task()
            [dataset(), code()] >> trainer

        return def_dag()


dag = IMDBTrainerDagBuilder().create_dag()
