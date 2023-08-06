from pipeline.pipeline import IngestionPipeline, PipelineStep


class SummaryStatistics(PipelineStep):
    def apply(self, pipeline: IngestionPipeline):
        """
        This step computes summary statistics for
        numeric attributes in the dataset.

        :param pipeline: parent IngestionPipeline
        :return:
        """
        numeric_attributes = [
            column
            for column in pipeline.column_type_map
            if pipeline.column_type_map[column] == "numeric"
        ]

        for attr in numeric_attributes:
            pipeline.summary_stats[attr] = (
                pipeline.df[attr].describe().to_dict()
            )  # noqa
