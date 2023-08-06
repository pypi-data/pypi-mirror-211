from ingestion.ingestion_pipeline_steps.interpreter_step import (  # noqa
    ColumnTypeInterpreter,
)
from pipeline.pipeline import IngestionPipeline
from sklearn.datasets import load_iris


def test_iris_types_numeric():
    pipeline = IngestionPipeline()
    pipeline.df = load_iris(return_X_y=True, as_frame=True)[0]
    pipeline.add(ColumnTypeInterpreter())
    pipeline.run()

    assert pipeline.column_type_map == {
        "sepal length (cm)": "numeric",
        "sepal width (cm)": "numeric",
        "petal length (cm)": "numeric",
        "petal width (cm)": "numeric",
    }
