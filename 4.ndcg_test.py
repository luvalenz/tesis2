import numpy as np
import random
import pandas as pd
from time_series import TimeSeriesOriginal
import dill
import time
import os
import sys
from scoring_utils import ndcg, Timer


def get_macho_class_from_path(path, classes):
    for c in classes:
        if c in path:
            return c
    return None


def sample_class(lcs_paths, class_name, n):
    class_paths = [path for path in lcs_paths if class_name in path]
    return random.sample(class_paths, n)


def get_macho_lightcurve(path):
    df = pd.read_csv(path, header=2, delimiter=' ')
    time = df['#MJD'].values
    magnitude = df['Mag'].values
    return TimeSeriesOriginal(time, magnitude, path)


def query(tree, lightcurve):
    timer = Timer()
    query_result = tree.make_query(lightcurve, timer)
    query_result = query_result.sort([0])
    elapsed = timer.elapsed_times
    return query_result.index, elapsed


def get_macho_class_from_path(path, classes):
    for c in classes:
        if c in path:
            return c
    return None


def query_ncdg(tree, lightcurve, classes, n):
    path = lightcurve._id
    class_ = get_macho_class_from_path(path, classes)
    retrieved, elapsed_time = query(tree, lightcurve)
    retrieved_classes = [get_macho_class_from_path(ret, classes) for ret in retrieved]
    scores = ndcg(retrieved_classes, class_, n)
    return scores, elapsed_time


def batch_queries(tree, lightcurves, classes, n):
    results = {}
    times = []
    for lc in lightcurves:
        result, elapsed_time = query_ncdg(tree, lc, classes, n)
        results[lc._id] = result
        times.append(elapsed_time)
    return results, times


if __name__ == '__main__':
    #LOAD SUBSEQUENCE TREE
    root = '/home/lucas/tesis2'
    #root = '/mnt/nas/GrimaRepo/luvalenz'
    model_name = sys.argv[1]#'sequence_tree_1000samples_20levels'
    samples_per_class = int(sys.argv[2])
    results_per_query = int(sys.argv[3])
    st_path = os.path.join(root, 'models/{0}.dill'.format(model_name))
    output_path = os.path.join(root,
                               'test_outputs/times_{0}_{1}samples_per_class_{2}results_per_query.dill'.format(
                                   model_name, samples_per_class, results_per_query
                               ))
    with open(st_path, 'rb') as f:
        tree = dill.load(f)
    with open('lightcurves.txt') as f:
        paths_list = f.readlines()
    paths_list = [os.path.join(root, path[:-1]) for path in paths_list]
    classes = ['BE', 'ML', 'NV', 'QSO', 'CEPH', 'EB', 'LPV', 'RRL']
    results = {}
    times = {}
    tree.calculate_inverted_files()
    for class_ in classes:
        print('running tests for class {0}'.format(class_))
        lcs_paths = sample_class(paths_list, class_, samples_per_class)
        lcs = [get_macho_lightcurve(path) for path in lcs_paths]
        results[class_], times[class_] = batch_queries(tree, lcs, classes, results_per_query)
    test_output = {'results': results, 'times': times}
    with open(output_path, 'wb') as f:
        dill.dump(test_output, f)


