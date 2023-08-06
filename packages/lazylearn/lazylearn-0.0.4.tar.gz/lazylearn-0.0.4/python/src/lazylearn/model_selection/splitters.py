import pandas as pd
from models.models import Dataset
from sklearn.model_selection import train_test_split


def test_train_splitter(
    dataset: Dataset, test_size: float, random_state=None
) -> Dataset:
    train_partition, test_partition = train_test_split(
        dataset.df, test_size=test_size, random_state=random_state
    )

    dataset.partitions["test"] = test_partition
    dataset.partitions["train"] = train_partition

    return dataset


def time_test_train_splitter(
    dataset: Dataset, test_size: float, split_date=None, split_column=None
) -> Dataset:
    n = len(dataset.df)

    df = dataset.df

    if split_date is not None:
        assert isinstance(split_date, pd.Timestamp)
        dataset.partitions["test"] = df[df[split_column] >= split_date]
        dataset.partitions["train"] = df[df[split_column] < split_date]

        return dataset

    if isinstance(test_size, float):
        test_size = int(n * test_size)
    elif isinstance(test_size, int):
        assert test_size < n
        # TODO: Implement a warning if test size seems too big

    dataset.partitions["test"] = df.tail(test_size)
    dataset.partitions["train"] = df.head(n - test_size)

    return dataset


def cv_splitter(dataset: Dataset) -> Dataset:
    return dataset
