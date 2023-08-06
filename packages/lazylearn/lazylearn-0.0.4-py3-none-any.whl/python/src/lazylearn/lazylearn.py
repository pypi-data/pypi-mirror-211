from typing import List, Tuple

import pandas as pd
from ingestion.ingestion_pipeline import Ingestion
from model_selection.splitters import (  # noqa
    test_train_splitter,
    time_test_train_splitter,
)
from models.models import Dataset
from pandas import DataFrame
from preprocessing.time.date_processor import date_processor
from preprocessing.time.duration import duration_builder
from regression.models.randomforest.randomforest import (  # noqa
    RandomForestRegressionRunner,
)
from strategies.strategy_builder import StrategyBuilder


class LazyLearner:
    """
    This class implements the LazyLearner, an object that
    runs AutoML for regression and classification given a
    dataset.

    To run an experiment with LazyLearn, instantiate the class,
    the add a dataset and configure the project through the
    create_project() method. To trigger the modelling process,
    call the run_autopilot() method with the desired mode.
    """

    def __init__(self, random_state=None):
        self.dataset: Dataset = None
        self.task: str = None
        self.models = None
        self._leaderboard = None
        self.random_state: int = random_state
        self.target: str = None
        self.metric = None
        self.otv_config: dict = None

    def create_project(
        self,
        data: DataFrame,
        target: str,
        task="infer",
        metric="default",
        test_size: float = 0.2,
        otv_config: dict = None,
    ):
        """
        Method to initialise a LazyLearn project.

        :param data: pandas DataFrame containing feature and target columns
        :param target: string of target column name
        :param task: "regression", "classification" or "infer"
        :param metric: metric by which to rank models
        :param test_size: share of dataset to use for holdout
        :param otv_config: out-of-time validation configuration of the form
            otv_config = {
                "column" = "column_to_time_partition_on",
                "holdout_start_date" = "YYYYMMDD"
            }
        :return:
        """
        # ingest data
        self.target = target
        self.dataset = Ingestion().run(data)

        if task == "infer":
            # if target is numeric then regression, else classification
            if self.dataset.column_type_map[target] == "numeric":
                self.task = "regression"
                if metric == "default":
                    self.metric = "mse"
            else:
                self.task = "classification"

        # process dates

        self.dataset = date_processor(self.dataset)
        self.dataset = duration_builder(self.dataset)

        # split partitions

        if otv_config is not None:
            assert (
                otv_config["column"]
                in self.dataset.type_collections["datetime"]  # noqa
            )
            self.otv_config = otv_config
            self.dataset.df = self.dataset.df.sort_values(
                by=self.otv_config["column"]
            )  # noqa

            self.dataset = time_test_train_splitter(
                self.dataset,
                test_size=test_size,
                split_date=pd.to_datetime(otv_config["holdout_start_date"]),
                split_column=otv_config["column"],
            )  # noqa
        else:
            self.dataset = test_train_splitter(
                self.dataset,
                test_size=test_size,
                random_state=self.random_state,  # noqa
            )

        # set modelling configurations

    def run_autopilot(self):
        """
        Trigger build and subsequent runs of modelling
        strategies.

        :return:
        """
        sb = StrategyBuilder(
            task=self.task,
            dataset=self.dataset,
            target=self.target,
            random_state=self.random_state,
        )
        self._leaderboard = sorted(
            [model for model in sb.models], key=lambda x: x.score[self.metric]
        )

    def leaderboard(self) -> List[Tuple[str, float]]:
        """
        Method to retrieve the sorted leaderboard of evaluated
        models.

        :return: List of tuples of model names and their scores
        """
        return [(item.name, item.score) for item in self._leaderboard]
