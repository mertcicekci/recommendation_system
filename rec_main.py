"""[summary]"""
from recom_system import *
import settings


def random_products(productid_list):
    res = np.random.choice(
        productid_list,
        size=np.random.randint(2, high=6),
        replace=False,
    )
    return res


def hayde(product_ids=None):
    # datalar İmport ediliyor

    if not os.path.exists(settings.db_path):
        if not os.listdir(settings.db_path):
            data = imp_exp.raw_data_importer(path=settings.data_path)
            # Popularity hesaplaması
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

    if product_ids == None:
        product_ids = random_products(
            productid_list=data["popularity_res"]["productid"].values
        )

    res_collob = collaborative_rec.get_collaborative_rec(
        fres_object=data["collaborative_result"], fcart_list=product_ids
    )
    res_content = content_based_rec.get_content_rec(
        fres_object=data["content_result"],
        fcart_list=product_ids,
        weight_dict=settings.weight_dict,
    )

    res_hybrid = hybrid_rec.get_hybrid_rec(
        ftbl_content=res_content,
        ftbl_collob=res_collob,
        ftbl_popularity=data["popularity_res"],
        weight_dict=settings.weight_dict,
    )
    return (
        res_hybrid,
        data["popularity_res"][data["popularity_res"]["productid"].isin(product_ids)]
        .drop(columns="popularity_score")
        .reset_index(drop=True),
    )
