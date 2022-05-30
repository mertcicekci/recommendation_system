"""This module is for import and export operations."""
from recom_system import *


def raw_data_importer(path):
    """
    This function reads raw data and stop words.
    Args:
        path (str): Path of data.
    Returns:
        res (dict): Dictionary of all data
    """
    # Reading .json files and converting them to Pandas dataframe
    meta_json = open(f"{path}/meta.json", encoding="utf8")
    events_json = open(f"{path}/events.json", encoding="utf8")
    events_df = pd.DataFrame(json.load(events_json)["events"])
    meta_df = pd.DataFrame(json.load(meta_json)["meta"])

    # missing control and manipulate or delete
    events_df.dropna(subset=["sessionid", "eventtime", "productid"], inplace=True)
    meta_df.dropna(subset=["name", "productid"], inplace=True)
    meta_df.fillna("", inplace=True)
    # read stop words.
    with open(f"{path}/stopwords.txt", "r", encoding="cp1254") as f:
        stop_words = f.read().split()
    events_json.close()
    meta_json.close()

    res = {
        "meta_df": meta_df,
        "events_df": events_df,
        "stop_words": stop_words,
    }

    return res


def exporter(ffile, fpath, file_type):
    """
    This function writes data to database.
    Args:
        ffile (class or Pandas Dataframe): Data to be written out.
        fpath (str): Output path.
        file_type (str): File type.
    """
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    if file_type == "pickle":
        with open(f"{fpath}/{ffile.__class__.__name__}.pkl", "wb") as outp:
            pickle.dump(ffile, outp, pickle.HIGHEST_PROTOCOL)
    else:
        ffile.to_parquet(f"{fpath}/popularity_res.parquet")


def res_importer(fpath):
    """
    This function reads data from database.
    Args:
        fpath (str): Database path.
    """
    file_list = os.listdir(fpath)
    res = {}
    for file in file_list:
        if file[-3:] == "pkl":
            with open(f"{fpath}/{file}", "rb") as imp:
                res.update({file[:-4]: pickle.load(imp)})
        else:
            data = pd.read_parquet(f"{fpath}/{file}")
            res.update({file[:-8]: data})

    return res