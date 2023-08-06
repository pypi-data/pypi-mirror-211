from pipeline.pipeline import PipelineStep, RegressionPipeline


class XGBRegressorStep(PipelineStep):
    def fit(self, pipeline: RegressionPipeline):
        pipeline.feature_list = [
            item for item in pipeline.feature_list if item != pipeline.target
        ]
        print("Fitting XGBRegressor")
        pipeline.regressor.fit(
            X=pipeline.train_features_df[pipeline.feature_list],
            y=pipeline.train_targets,
        )  # noqa
        print("XGBRegressor fitted!")

    def predict(self, pipeline: RegressionPipeline):
        pipeline.tmp_pred = pipeline.regressor.predict(
            X=pipeline.tmp_test[pipeline.feature_list]
        )
