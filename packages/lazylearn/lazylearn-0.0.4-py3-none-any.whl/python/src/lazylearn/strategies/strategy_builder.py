from models.models import Model
from regression.models.randomforest.randomforest import (  # noqa
    RandomForestRegressionRunner,
)
from regression.models.xgboost.xgb import XGBRegressionRunner
from strategies.strategy_steps.evaluation import Evaluator


class StrategyBuilder:
    def __init__(self, task, dataset, target, random_state=None):
        self.task = task
        self.dataset = dataset
        self.target = target
        self.random_state = random_state
        self.strategies = []
        self.models = []

        self.build()
        self.start()

    def build(self):
        if self.task == "regression":
            self.strategies.append(
                XGBRegressionRunner(
                    target=self.target,
                    dataset=self.dataset,
                    random_state=self.random_state,  # noqa
                )
            )
            self.strategies.append(
                RandomForestRegressionRunner(
                    target=self.target,
                    dataset=self.dataset,
                    random_state=self.random_state,  # noqa
                )
            )

        else:
            raise ValueError("Unsupported task!")

    def start(self):
        for strategy in self.strategies:
            strategy.fit()

            # get holdout scores
            strategy.predict(self.dataset.partitions["test"].copy())
            strategy.pipeline.holdout_score = Evaluator().evaluate(
                self.task,
                self.dataset.partitions["test"][self.target],
                strategy.pipeline.tmp_pred,
            )

            self.models.append(
                Model(
                    name=strategy.name,
                    score=strategy.pipeline.holdout_score,
                    pipeline=strategy,
                )
            )
