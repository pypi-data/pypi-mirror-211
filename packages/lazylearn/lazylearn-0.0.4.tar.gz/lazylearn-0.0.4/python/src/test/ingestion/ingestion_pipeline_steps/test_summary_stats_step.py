import pandas as pd
from ingestion.ingestion_pipeline_steps.summary_stats_step import (  # noqa
    SummaryStatistics,
)
from pipeline.pipeline import IngestionPipeline
from sklearn.datasets import load_iris


def test_iris_stats():
    pipeline = IngestionPipeline()
    pipeline.df = pd.concat(load_iris(return_X_y=True, as_frame=True), axis=1)
    pipeline.column_type_map = {
        "sepal length (cm)": "numeric",
        "sepal width (cm)": "numeric",
        "petal length (cm)": "numeric",
        "petal width (cm)": "numeric",
    }

    pipeline.add(SummaryStatistics())
    pipeline.run()

    expected_stats = {
        "min": 1,
        "max": 6.9,
        "25%": 1.6,
        "50%": 4.35,
        "75%": 5.1,
        "mean": 3.758,
        "std": 1.765,
    }

    for stat in expected_stats:
        assert expected_stats[stat] == round(
            pipeline.summary_stats["petal length (cm)"][stat], 3
        )
