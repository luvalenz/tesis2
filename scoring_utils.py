import numpy as np
import time

def relevance(retrieved_labels, relevant_label):
    return np.array(retrieved_labels) ==  relevant_label


def dcg(relevance):
    index = np.arange(len(relevance))
    discount = np.log2(index + 2)
    term = (2**relevance-1)/discount
    return np.cumsum(term)


def ndcg(retrieved, relevant_label, n):
    rel_true = relevance(retrieved, relevant_label)
    rel_ideal = np.sort(rel_true)[::-1]
    dcg_score = dcg(rel_true)
    idcg_score = dcg(rel_ideal)
    ndcg_score = dcg_score/idcg_score
    length = len(ndcg_score)
    if n <= length:
        ndcg_score = ndcg_score[:n]
    else :
        padding = n - length
        print(padding)
        ndcg_score = np.concatenate((ndcg_score, -1*np.ones(padding)))
    return ndcg_score





class Timer:

    def __init__(self):
        self.elapsed_times = []
        self.current_start = None

    def start(self):
        self.current_start = time.time()

    def stop(self):
        current = time.time()
        elapsed = current - self.current_start
        self.elapsed_times.append(elapsed)