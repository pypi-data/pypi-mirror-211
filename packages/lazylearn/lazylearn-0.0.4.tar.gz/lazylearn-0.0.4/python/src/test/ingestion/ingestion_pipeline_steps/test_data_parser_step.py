from ingestion.ingestion_pipeline_steps.data_parser_step import DataSourceParser  # noqa
from pipeline.pipeline import IngestionPipeline
from sklearn.datasets import load_iris


def test_iris_okay():
    pipeline = IngestionPipeline()
    pipeline.raw_data = load_iris(return_X_y=True, as_frame=True)[0]
    pipeline.add(DataSourceParser())
    pipeline.run()

    assert pipeline.raw_data.equals(pipeline.df)
