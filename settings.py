"""Program settings file"""

# Data base paths
data_path = "data"
db_path = "db"


# Dictionary of weighting parameters.
weight_dict = {
    "content": 0.35,
    "collaborative": 0.55,
    "popularity": 0.1,
    "tfidf": 0.25,
    "count": 0.75,
}