"""Main recommendation system module"""
from recom_system import *
import settings


def random_products(productid_list):
    """
    Prepares a random product list.
    Args:
        productid_list (list): List of all products.
    Returns:
        res (list): Random product list.
    """
    res = np.random.choice(
        productid_list,
        size=np.random.randint(2, high=6),
        replace=False,
    )
    return res


def db_control(path):
    """
    Checks the existence of database files.
    Args:
        path (str): Database path.
    Returns:
        res (bool): True if there are no files.
    """
    if os.path.exists(path):
        if len(os.listdir(path)) == 3:
            return False
    return True


def rec_proc(product_ids=None):
    """
    It runs the entire recommendation process.

    Args:
        product_ids (List): List of products.
    Returns:
        res (tuple): Tuple for final recommendations table and cart page.
    """

    # If the program is run for the first time, it extracts the necessary files to the db folder.
    if db_control(path=settings.db_path):
        data = imp_exp.raw_data_importer(path=settings.data_path)

        popularity_rec.calc_popularity(
            ftbl_meta=data["meta_df"].copy(),
            ftbl_events=data["events_df"].copy(),
            fpath=settings.db_path,
        )
        content_based_rec.calc_content_rec(
            ftbl=data["meta_df"].copy(),
            stop_words=data["stop_words"],
            fpath=settings.db_path,
        )
        collaborative_rec.calc_collaborative_rec(
            ftbl_meta=data["meta_df"].copy(),
            ftbl_events=data["events_df"].copy(),
            fpath=settings.db_path,
        )
        del data

    data = imp_exp.res_importer(fpath=settings.db_path)
    # If the user has not made a product id list, it is randomly generated.
    if product_ids == None:
        product_ids = random_products(
            productid_list=data["popularity_res"]["productid"].values
        )

    # The recommendations of the methods are tabulated.
    res_collob = collaborative_rec.get_collaborative_rec(
        fres_object=data["collaborative_result"], fcart_list=product_ids
    )
    res_content = content_based_rec.get_content_rec(
        fres_object=data["content_result"],
        fcart_list=product_ids,
        weight_dict=settings.weight_dict,
    )
    # After weighting the results of all these approaches, the final recommendations are reached.
    res_hybrid = hybrid_rec.get_hybrid_rec(
        ftbl_content=res_content,
        ftbl_collob=res_collob,
        ftbl_popularity=data["popularity_res"],
        weight_dict=settings.weight_dict,
    )

    res = (
        res_hybrid,
        data["popularity_res"][data["popularity_res"]["productid"].isin(product_ids)]
        .drop(columns="popularity_score")
        .reset_index(drop=True),
    )
    return res
