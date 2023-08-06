from typing import Dict

from pandas import DataFrame


class Dataset:
    def __init__(
        self,
        df: DataFrame,
        column_type_map: dict,
        summary_stats: dict,
        type_collections: dict,
    ):
        self.name = None
        self.description = None
        self.df: DataFrame = df
        self.column_type_map = column_type_map
        self.summary_stats = summary_stats
        self.type_collections = type_collections
        self.partitions: dict = {}

    def save(self):
        raise NotImplementedError


class Model:
    def __init__(self, name: str, score: Dict[str, float], pipeline):
        self.name = name
        self.score = score
        self.pipeline = pipeline

    def save(self, path: str):
        raise NotImplementedError


class Project:
    def __init__(self):
        self.name = None
        self.description = None

    def save(self, path: str):
        raise NotImplementedError
