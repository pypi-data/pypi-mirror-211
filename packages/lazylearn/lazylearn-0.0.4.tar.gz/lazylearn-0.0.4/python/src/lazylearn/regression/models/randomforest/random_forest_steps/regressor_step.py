from pipeline.pipeline import PipelineStep, RegressionPipeline
from sklearn.ensemble import RandomForestRegressor


class RandomForestRegressorStep(PipelineStep):
    def __init__(self, random_state=None):
        self.regressor = RandomForestRegressor(random_state=random_state)

    def fit(self, pipeline: RegressionPipeline):
        pipeline.feature_list = [
            item for item in pipeline.feature_list if item != pipeline.target
        ]
        print("Fitting RandomForestRegressor")
        self.regressor.fit(
            X=pipeline.train_features_df[pipeline.feature_list],
            y=pipeline.train_targets,
        )  # noqa
        print("RandomForestRegressor fitted!")

    def predict(self, pipeline: RegressionPipeline):
        pipeline.tmp_pred = self.regressor.predict(
            X=pipeline.tmp_test[pipeline.feature_list]
        )
