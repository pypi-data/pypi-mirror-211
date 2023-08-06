import pandas as pd
from errors.errors import DataSourceError
from ingestion.utils.csv import csv_check
from pandas import DataFrame
from pipeline.pipeline import IngestionPipeline, PipelineStep


class DataSourceParser(PipelineStep):
    def apply(self, pipeline: IngestionPipeline):
        """
        This method is responsible for parsing the raw data
        source from its parent pipeline into a DataFrame
        object.

        :param pipeline: parent IngestionPipeline
        :return:
        """
        assert pipeline.raw_data is not None

        if isinstance(pipeline.raw_data, DataFrame):
            pipeline.df = pipeline.raw_data
        # check if raw data is a path to a csv file and read it into csv
        elif csv_check(pipeline.df):
            pipeline.df = pd.read_csv(pipeline.raw_data)
        else:
            raise DataSourceError
