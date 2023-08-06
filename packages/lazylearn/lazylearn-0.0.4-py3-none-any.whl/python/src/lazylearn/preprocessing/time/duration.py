from models.models import Dataset


def duration_builder(dataset: Dataset) -> Dataset:
    """

    :param dataset:
    :return:
    """
    date_cols = dataset.type_collections.get("datetime")

    if len(date_cols) > 1:
        for i in range(len(date_cols)):
            for j in range(i + 1, len(date_cols)):
                col_name = f"duration({date_cols[i]}-{date_cols[j]})"
                dataset.df[col_name] = (
                    (dataset.df[date_cols[i]] - dataset.df[date_cols[j]])
                    .astype("timedelta64[D]")
                    .astype(int)
                )
                dataset.column_type_map[col_name] = "numeric"
                dataset.type_collections["numeric"].append(col_name)

    return dataset
