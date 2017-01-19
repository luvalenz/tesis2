from scoring_utils import Timer, ndcg
from scipy import stats


class QueryResult:

    def __init__(self, target, ranking, times):
        self.target = target
        self.ranking = ranking
        self.times = times
        
    @property
    def preprocessed_ranking(self):
        pr = []
        for e in self.ranking:
           pr.append(e[3:] if e.startswith('lc_') else e)
        return pr

    def ndcg(self, class_table):
        target_class = class_table.loc[self.target, 'class']
        ranking_classes = class_table.loc[self.preprocessed_ranking]['class'].values
        return target_class, ndcg(ranking_classes, target_class, len(ranking_classes))

    def kendall_tau(self, other_query_result):
        return stats.kendalltau(self.preprocessed_ranking, other_query_result.ranking)

    def __len__(self):
        return len(self.preprocessed_ranking)


class SubseuquenceSearcher:

    data_type = 'float64'

    def __init__(self, subseuquence_tree):
        self.st = subseuquence_tree

    def query(self, time_series):
        timer = Timer()
        result = self.st.make_query(time_series, timer)
        ranking = result.index.tolist()
        times = timer.elapsed_times
        return QueryResult(time_series.id, ranking, times)

