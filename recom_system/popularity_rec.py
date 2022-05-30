"""Popularity based recommendation system module"""
from recom_system import *


def calc_popularity(ftbl_meta, ftbl_events, fpath):
    """
    Date weighting is done according to the dates in the events data.
    The total number of events of the products is calculated.
    Then these total numbers are multiplied by the weighting values.
    The most selected products in recent days are assumed to be more popular, thus generating popularity scores.

    Args:
        ftbl_meta (Pandas DataFrame): Meta DataFrame.
        ftbl_events (Pandas DataFrame): Events DataFrame.
        fpath (str): Output path.

    """
    ftbl_events["time_weighting"] = pd.to_datetime(ftbl_events["eventtime"]).map(
        lambda x: x.year + x.month / 10
    )
    time_unique = ftbl_events["time_weighting"].sort_values().unique()
    time_unique_len = len(time_unique)
    mapping_dict = dict(
        zip(
            time_unique,
            [
                *np.arange(
                    1 / time_unique_len, 1 + 1 / time_unique_len, 1 / time_unique_len
                )
            ],
        )
    )
    ftbl_events["time_weighting"] = ftbl_events["time_weighting"].map(mapping_dict)

    time_weighting_df = (
        ftbl_events.groupby("productid")["time_weighting"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    time_weighting = time_weighting_df["time_weighting"].values
    time_weighting_df["time_weighting_normalized"] = (
        time_weighting - min(time_weighting)
    ) / (max(time_weighting) - min(time_weighting))

    res_popularity = time_weighting_df[["productid", "time_weighting_normalized"]]
    res_popularity = res_popularity.merge(ftbl_meta, how="left")
    res_popularity.rename(
        columns={"time_weighting_normalized": "popularity_score"}, inplace=True
    )

    imp_exp.exporter(ffile=res_popularity, fpath=fpath, file_type="parquet")
