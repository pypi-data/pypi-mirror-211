import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from pipeline.pipeline import IngestionPipeline
from tqdm import tqdm


class ColumnTypeInterpreter:
    def __int__(self):
        self.df: DataFrame = None

    def apply(self, pipeline: IngestionPipeline):
        """
        This method is responsible for inferring the
        types of the columns of the project dataset

        :param pipeline: parent IngestionPipeline
        :return:
        """
        self.df = pipeline.df
        columns = pipeline.df.columns
        column_types = {}

        for column_name in tqdm(columns):
            column_types[column_name] = self.analyze_column(
                pipeline.df[column_name]
            )  # noqa

        pipeline.column_type_map = column_types
        if "unknown" in pipeline.column_type_map.values():
            pipeline.needs_type_map = True

        pipeline.type_collections = self.build_type_collections(column_types)

    def analyze_column(self, column: Series):
        """

        :param column:
        :return:
        """
        values = column.tolist()
        types = [type(value) for value in values]

        column_type = None

        if self.categorical_test(values):
            column_type = "categorical"
        elif self.numeric_test(types) and self.id_check(types, values):
            column_type = "id"
        elif self.numeric_test(types):
            column_type = "numeric"

        if self.datetime_check(column) and not self.numeric_test(types):
            column_type = "datetime"

        if column_type is None:
            column_type = "unknown"

        return column_type

    @staticmethod
    def categorical_test(values: list):
        """
        Tests whether a column is of categorical type.
        This is decided as the case if the number of unique values is
        less than 5% of the total number of values in the column.

        :param values: list of values of any type
        :return: True if column is categorical, False otherwise
        """
        n_total = len(values)
        n_unique = len(set(values))
        percentage_unique = n_unique / n_total

        if percentage_unique < 0.05:
            return True
        return False

    @staticmethod
    def numeric_test(types: list):
        """
        Tests whether a column is of numeric tyoe.
        This is decided as the case if all values
        of a column is either float or int.

        :param types: list of type objects
        :return: True if column is numeric, False otherwise
        """
        return all(
            [
                item == float or item == int
                for item in set(types)
                if item is not None  # noqa
            ]
        )

    @staticmethod
    def string_test(types: set):
        raise NotImplementedError

    def datetime_check(self, column: Series):
        """

        :param column:
        :return:
        """
        col_name = str(column.name)

        # if type of column is actually datetime
        if self.df[col_name].dtype.type == np.datetime64:
            return True

        # if date or time is in column name and can be cast as date
        if "date" in col_name.lower() or "time" in col_name.lower():
            try:
                self.df[col_name] = pd.to_datetime(self.df[col_name])
                return True
            except Exception as e:  # noqa
                pass

        # if format of values looks like dates

        return False

    def id_check(self, types, values):
        """

        :param types:
        :param values:
        :return:
        """
        return all(
            [item == int for item in set(types) if item is not None]
        ) and len(  # noqa
            set(values)
        ) == len(
            self.df
        )

    @staticmethod
    def build_type_collections(column_type_map):
        collections = {}

        for data_type in ["datetime", "numeric", "categorical"]:
            collections[data_type] = [
                col
                for col in column_type_map
                if column_type_map[col] == data_type  # noqa
            ]

        return collections
