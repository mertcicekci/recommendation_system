"""Content based recommendation system module"""
from recom_system import *


class content_result(object):
    def __init__(self, cosine_sim_text_combine, cosine_sim_name, indices):
        self.cosine_sim_text_combine = cosine_sim_text_combine
        self.cosine_sim_name = cosine_sim_name
        self.indices = indices


def calc_content_rec(ftbl, stop_words, fpath):
    """
    Calculates the number of days or the date for TermCds.

    Args:
        ftbl_meta (Pandas DataFrame): Meta DataFrame.
        stop_words (List): Stop words list.
        fpath (str): Output path.

    """
    # also remove @,%,#, and other special characters
    ftbl["brand"] = ftbl["brand"].apply(lambda x: re.sub(r"[^\w\s]", "", x.lower()))
    ftbl["category"] = ftbl["category"].apply(
        lambda x: re.sub(r"[^\w\s]", "", x.lower())
    )
    ftbl["subcategory"] = ftbl["subcategory"].apply(
        lambda x: re.sub(r"[^\w\s]", "", x.lower())
    )

    ftbl["text_combine"] = (
        ftbl["brand"] + " " + ftbl["category"] + " " + ftbl["subcategory"]
    )
    ftbl.drop(["brand", "category", "subcategory"], axis=1, inplace=True)

    vectorized = TfidfVectorizer(stop_words=stop_words)
    matrix = vectorized.fit_transform(ftbl["name"])
    cosine_sim_name = np.array(cosine_similarity(matrix))

    ftbl = ftbl.reset_index()
    indices = pd.Series(ftbl.index, index=ftbl["productid"])

    count_vectorized = CountVectorizer(stop_words=stop_words)
    count_matrix = count_vectorized.fit_transform(ftbl["text_combine"])
    cosine_sim_text_combine = np.array(cosine_similarity(count_matrix))

    res = content_result(cosine_sim_text_combine, cosine_sim_name, indices)
    imp_exp.exporter(ffile=res, fpath=fpath, file_type="pickle")


def get_content_rec(fres_object, fcart_list, weight_dict):
    """
    A recommendation table is created from the trained data.

    Args:
        fres_object (class): Class of trained data
        fcart_list (List): List of products.
        weight_dict (dict): Dictionary of weighting parameters.
    Returns:
        res_content (Pandas DataFrame): content-based recommendations table.
    """

    weighted_similarity = (
        weight_dict["count"] * fres_object.cosine_sim_text_combine
        + weight_dict["tfidf"] * fres_object.cosine_sim_name
    )

    scores_list = []
    product_list = []
    for product_id in fcart_list:
        idx = fres_object.indices[product_id]
        product_list.append(idx)
        sim_scores = list(enumerate(weighted_similarity[idx]))
        scores_list.extend(sim_scores)

    sorted_scores = sorted(scores_list, key=lambda x: x[1], reverse=True)

    product_indices = []
    product_scores = []
    for score in sorted_scores:
        if len(product_indices) == 10:
            break
        if score[0] not in product_list and score[0] not in product_indices:
            product_indices.append(score[0])
            product_scores.append(score[1])

    scores_df = pd.DataFrame(
        {"product_scores": product_scores, "product_indices": product_indices}
    )
    res_content = scores_df.merge(
        fres_object.indices[fres_object.indices.isin(product_indices)].reset_index(),
        how="left",
        left_on="product_indices",
        right_on=0,
    )[["product_scores", "productid"]]

    res_content.rename(columns={"product_scores": "rec_score"}, inplace=True)

    return res_content
