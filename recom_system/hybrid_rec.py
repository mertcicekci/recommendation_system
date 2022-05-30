"""Hybrid recommendation system module"""
from recom_system import *


def get_hybrid_rec(ftbl_content, ftbl_collob, ftbl_popularity, weight_dict):
    """
    After weighting the results of all these approaches(Content-Based,Collaborative,Popularity), the final recommendations are reached.

    Args:
        ftbl_content (Pandas DataFrame): Meta DataFrame.
        ftbl_collob (Pandas DataFrame): Meta DataFrame.
        ftbl_popularity (Pandas DataFrame): Meta DataFrame.
        weight_dict (dict): Dictionary of weighting parameters.


    Returns:
        res (Pandas DataFrame): Final recommendations table.
    """

    ftbl_content["rec_score"] = ftbl_content["rec_score"] * weight_dict["content"]
    ftbl_collob["rec_score"] = ftbl_collob["rec_score"] * weight_dict["collaborative"]

    weighted_score_df = pd.concat([ftbl_content, ftbl_collob])
    popularity_df = ftbl_popularity[
        ftbl_popularity["productid"].isin(weighted_score_df["productid"].values)
    ]
    popularity_df["rec_score"] = (
        popularity_df["popularity_score"].values * weight_dict["popularity"]
    )
    weighted_score_df = pd.concat([weighted_score_df, popularity_df])

    weighted_score_df = (
        weighted_score_df.groupby("productid")["rec_score"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    res = weighted_score_df.merge(
        popularity_df[["productid", "brand", "category", "subcategory", "name"]],
        how="left",
    ).head(10)

    return res