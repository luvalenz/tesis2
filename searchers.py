import glob2
import os
import pandas as pd
from sklearn.neighbors import KDTree
import numpy as np
import time
from scoring_utils import Timer


class QueryResult:

    def __init__(self, ranking, times):
        self.ranking = ranking
        self.times = times


class SubseuquenceSearcher(object):

    data_type = 'float64'

    def __init__(self, subseuquence_tree):
        self.st = subseuquence_tree

    def query(self, time_series):
        timer = Timer()
        result = self.st.make_query(time_series, timer)
        ranking = result.index.tolist()
        times = timer.elapsed_times
        return QueryResult(ranking, times)

