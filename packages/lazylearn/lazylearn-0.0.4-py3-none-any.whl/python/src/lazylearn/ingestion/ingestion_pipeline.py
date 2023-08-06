from ingestion.ingestion_pipeline_steps.data_parser_step import DataSourceParser  # noqa
from ingestion.ingestion_pipeline_steps.interpreter_step import (  # noqa
    ColumnTypeInterpreter,
)
from ingestion.ingestion_pipeline_steps.summary_stats_step import (  # noqa
    SummaryStatistics,
)
from pipeline.pipeline import IngestionPipeline


class Ingestion:
    def __init__(self):
        pass

    def run(self, data):
        """

        :param data:
        :return:
        """
        pipeline = IngestionPipeline()
        pipeline.raw_data = data

        pipeline.add(DataSourceParser())

        pipeline.add(ColumnTypeInterpreter())

        pipeline.add(SummaryStatistics())

        pipeline.run()

        return pipeline.response()
