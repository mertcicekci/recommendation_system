from recom_system import *


class collaborative_result(object):
    def __init__(self, productid, cosine_sim_matrix):
        self.productid = productid
        self.cosine_sim_matrix = cosine_sim_matrix


def calc_collaborative_rec(ftbl_meta, ftbl_events, fpath):
    data = ftbl_meta.merge(ftbl_events, on="productid")
    data = data[["sessionid", "productid", "event", "eventtime"]]

    data["eventdate"] = pd.to_datetime(data["eventtime"]).map(lambda x: x.date())
    data["cartid"] = data["sessionid"] + data["eventdate"].astype(str)
    data.drop_duplicates(subset=["cartid", "productid"], inplace=True)

    cart_list = (
        data.groupby("cartid")["productid"].apply(list).reset_index(name="cart_list")
    )
    data = data.merge(cart_list, how="left")
    data = data.explode(column="cart_list")
    data = data.drop_duplicates(subset=["productid", "cart_list"])

    product_cat = CategoricalDtype(sorted(data.productid.unique()), ordered=True)
    cart_cat = CategoricalDtype(sorted(data.cart_list.unique()), ordered=True)
    row = data.productid.astype(product_cat).cat.codes
    col = data.cart_list.astype(cart_cat).cat.codes
    data["event"] = 1
    cart_item_matrix = csr_matrix(
        (data["event"], (row, col)),
        shape=(product_cat.categories.size, cart_cat.categories.size),
    )

    cosine_sim_matrix = cosine_similarity(cart_item_matrix, dense_output=False)
    res = collaborative_result(product_cat.categories, cosine_sim_matrix)
    imp_exp.exporter(ffile=res, fpath=fpath, file_type="pickle")


def get_collaborative_rec(fres_object, fcart_list):

    res = pd.DataFrame()
    for product in fcart_list:
        session_series = pd.Series(fres_object.productid)
        id = session_series[session_series == product].index.values[0]

        frame = pd.DataFrame(fres_object.cosine_sim_matrix[id].todense()).T.sort_values(
            by=0, ascending=False
        )
        frame = frame.reset_index()
        frame.columns = ["id", "similarity"]
        frame[f"session_id"] = session_series.loc[frame["id"].values].values
        res = pd.concat([res, frame])

    res_session = res.sort_values(by="similarity", ascending=False).rename(
        columns={"similarity": "rec_score", "session_id": "productid"}
    )
    res_session = res_session[~res_session["productid"].isin(fcart_list)]

    return res_session