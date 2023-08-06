from models.models import Dataset


def date_processor(dataset: Dataset) -> Dataset:
    """
    Method that transform date variables into
    categorical features.

    :param dataset: Dataset object with date features
    :return: Dataset object with categorical date
    features
    """
    new_categorical_cols = []

    for date_column in dataset.type_collections["datetime"]:
        dataset.df[f"{date_column}_year"] = (
            dataset.df[date_column].dt.isocalendar().year
        )
        dataset.df[f"{date_column}_month"] = dataset.df[date_column].dt.month
        dataset.df[f"{date_column}_week"] = (
            dataset.df[date_column].dt.isocalendar().week
        )
        dataset.df[f"{date_column}_day"] = (
            dataset.df[date_column].dt.isocalendar().day
        )  # noqa

        new_categorical_cols.append(f"{date_column}_year")
        new_categorical_cols.append(f"{date_column}_month")
        new_categorical_cols.append(f"{date_column}_week")
        new_categorical_cols.append(f"{date_column}_day")

    for cat in new_categorical_cols:
        dataset.column_type_map[cat] = "categorical"
        dataset.type_collections["categorical"].append(cat)

    return dataset
