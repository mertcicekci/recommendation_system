from recom_system import *


def raw_data_importer(path):

    # .json uzantılı dosyaları okuyoruz ve Pandas dataframe e dönüşütürüyoruz.
    meta_json = open(f"{path}/meta.json", encoding="utf8")
    events_json = open(f"{path}/events.json", encoding="utf8")
    events_df = pd.DataFrame(json.load(events_json)["events"])
    meta_df = pd.DataFrame(json.load(meta_json)["meta"])

    # missing veriler uçuruluyor ya da değiştiriliyor.
    events_df.dropna(subset=["sessionid", "eventtime", "productid"], inplace=True)
    meta_df.dropna(subset=["name", "productid"], inplace=True)
    meta_df.fillna("", inplace=True)
    # stopwords okunuyor.
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

    if not os.path.exists(fpath):
        os.makedirs(fpath)
    if file_type == "pickle":
        with open(f"{fpath}/{ffile.__class__.__name__}.pkl", "wb") as outp:
            pickle.dump(ffile, outp, pickle.HIGHEST_PROTOCOL)
    else:
        ffile.to_parquet(f"{fpath}/popularity_res.parquet")


def res_importer(fpath):

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