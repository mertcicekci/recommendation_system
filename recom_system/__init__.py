"""Contains modules for recommendations."""

# Required libraries
import pandas as pd
import numpy as np
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from pandas.api.types import CategoricalDtype
import pickle
import os

# Modules of the program
from . import imp_exp
from . import content_based_rec
from . import collaborative_rec
from . import popularity_rec
from . import hybrid_rec