from pandas import DataFrame
from pipeline.pipeline import ModelPipeline


class OrdinalConverter:
    def __init__(
        self,
        cat_vars: list,
        max_cardinality: int = None,
        min_support: int = 5,
        other_category: bool = True,
        method: str = "freq",
    ):
        self.cat_vars = cat_vars
        self.card_max = max_cardinality
        self.min_support = min_support
        self.other_category = other_category
        self.method = method
        self.cat_freqs = {}
        self.cat_maps = {}

    def fit(self, pipeline: ModelPipeline):
        for var in self.cat_vars:
            pipeline.train_features_df = self.convert(
                pipeline.train_features_df, var
            )  # noqa
            pipeline.feature_list.append(var)

    def convert(self, df: DataFrame, col_name: str) -> DataFrame:
        """
        Encodes a categorical column ordinally.
        Currently only the "freq" method is supported,
        and it encodes a value with an integer id by
        increasing frequency i.e. more frequent values
        receive a higher encoding

        Note that this should only be done on the training
        data!

        :param df: pandas DataFrame of features
        :param col_name: column to consider
        :return: transformed DataFrame
        """
        if self.method == "freq":
            self.cat_freqs[col_name] = {}
            for item in df[col_name].tolist():
                if item in self.cat_freqs[col_name]:
                    self.cat_freqs[col_name][item] += 1
                else:
                    self.cat_freqs[col_name][item] = 1

            freq_pairs = sorted(
                [(key, val) for key, val in self.cat_freqs[col_name].items()],
                key=lambda x: x[1],
            )

            self.cat_maps[col_name] = {key: val for key, val in freq_pairs}

            df[col_name] = df[col_name].apply(
                lambda x: self.cat_maps[col_name][x]
                if self.cat_maps[col_name][x] >= self.min_support
                else -1
            )
            return df
        else:
            raise ValueError("Unsupported encoding method, try [freq]")

    def predict(self, pipeline: ModelPipeline):
        df = pipeline.tmp_test

        for var in self.cat_vars:
            df[var] = df[var].apply(
                lambda x: self.cat_maps[var][x]
                if x in self.cat_maps[var]
                else -2  # noqa
            )

        pipeline.tmp_test = df
