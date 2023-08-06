from typing import List

from models.models import Dataset
from pandas import DataFrame, Series


class Pipeline:
    def __init__(self):
        self._has_run: bool = False
        self._steps: List[PipelineStep] = []

    def add(self, pipeline_step):
        self._steps.append(pipeline_step)

    def run(self):
        [step.apply(self) for step in self._steps]
        self._has_run = True


class PipelineStep:
    def apply(self, pipeline: Pipeline):
        pass

    def fit(self, pipeline: Pipeline):
        pass

    def predict(self, pipeline: Pipeline):
        pass


class IngestionPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.raw_data = None
        self.df: DataFrame = None
        self.column_type_map: dict = None
        self.summary_stats: dict = {}
        self.needs_type_map: bool = False
        self.type_collections: dict = None

    def response(self):
        return Dataset(
            df=self.df,
            column_type_map=self.column_type_map,
            summary_stats=self.summary_stats,
            type_collections=self.type_collections,
        )


class ModelPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self._is_fitted = False
        self.feature_list: list = []
        self.tmp_test = None
        self.tmp_pred = None
        self.target = None

    def fit(self):
        [step.fit(self) for step in self._steps]
        self._is_fitted = True

    def predict(self):
        assert self._is_fitted
        [step.predict(self) for step in self._steps]
        return self.tmp_pred


class RegressionPipeline(ModelPipeline):
    def __init__(self):
        super().__init__()
        self.train_features_df: DataFrame = None
        self.train_targets: Series = None
        self.holdout_features_df: DataFrame = None
        self.holdout_targets: Series = None
        self.holdout_score: float = None
        self.regressor = None
