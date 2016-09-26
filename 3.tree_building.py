from subsequence_tree import SubsequenceTree
import pickle
import dill
import pandas as pd
from time_series import TimeSeriesOriginal, TimeSeriesSubsequence
import numpy as np
import glob2 as glob
import os
import sys


def get_macho_dataset(root, max_files=None):
    paths = glob.iglob(os.path.join(root, '**/*.mjd'))
    if max_files is not None:
        paths = list(paths)[:max_files]
    lightcurves = (get_macho_lightcurve(file_path)
                   for file_path in paths)
    return lightcurves


def get_macho_lightcurve(path):
    df = pd.read_csv(path, header=2, delimiter=' ')
    print(path)
    time = df['#MJD'].values
    magnitude = df['Mag'].values
    return TimeSeriesOriginal(time, magnitude, get_macho_relative_path(path), True)


def get_macho_relative_path(path):
    start = path.find('macho_training_lightcurves')
    if start == -1:
        start = path.find('MACHO training lightcurves')
    path = path[start:]
    return path[path.find('/') + 1:]


def results_are_equal(r1, r2):
    r1 = r1.values
    r2 = r2.values
    return np.all(r1 - r2 < 1e-3)


def get_macho_prototypes(sample_path):
    with open(sample_path, 'rb') as f:
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        sample = u.load()
    for path, magnitude, time in zip(*sample):
        print(path)
        relative_path = get_macho_relative_path(path)
        print(relative_path)
        yield TimeSeriesSubsequence(time, magnitude, relative_path, relative_path)


def get_macho_lucas_prototypes(sample_path):
    with open(sample_path, 'rb') as f:
        prototypes = pickle.load(f)
    return prototypes


def build_tree(sample_path, affinities_path, db_path,
               output_path, max_level, clustering_threshold,
               weighted=True):
    #prototypes =  list(get_macho_prototypes(sample_path))
    prototypes =  list(get_macho_lucas_prototypes(sample_path))
    npzfile = np.load(affinities_path)
    distances = npzfile[npzfile.files[0]]
    affinities = - distances**2
    dataset = get_macho_dataset(db_path)
    print('building tree...')
    st = SubsequenceTree(max_level, prototypes, affinities, dataset, clustering_threshold,
                         weighted)
    for s in st.node_shortcuts:
        if s.is_leaf:
            print(s.n_original_time_series_in_node)
    for s in st.node_shortcuts:
        if s.is_leaf:
            print(s.inverted_file)
    with open( output_path, 'wb' ) as f:
        dill.dump(st,  f)


if __name__ == '__main__':
    #root_path = '/home/lucas/tesis2'
    root_path = '/mnt/nas/GrimaRepo/luvalenz'
    lc_list_path = sys.argv[1]
    n = int(sys.argv[2])
    semi_standardize = False
    standardize = False
    weighted = True
    window_size = 250
    step = 10
    max_level = 20
    if len(sys.argv) > 3:
        if sys.argv[3] == 'semi':
            semi_standardize = True
            print('semi standarized')
        if sys.argv[3] == 'std':
            standardize = True
            print('standarized')
    if len(sys.argv) > 4:
        if sys.argv[4] == 'not':
            weighted = False
            print('not weighted tree')
    if len(sys.argv) > 5:
        window_size = int(sys.argv[5])
        step = int(sys.argv[6])
        max_level = int(sys.argv[7])
    mac_data_path = os.path.join(root_path, 'mackenzie_data/')
    lucas_data_path = os.path.join(root_path, 'lucas_data/')
    db_path = os.path.join(root_path, 'macho_training_lightcurves')
    output_path = os.path.join(root_path, 'models')
    distances_path = os.path.join(lucas_data_path, 'subsequences_distances_{0}_n={1}_semistd{2}_std{3}_window{4}_step{5}.npz'.format(lc_list_path, n, semi_standardize, standardize, window_size, step))
    sample_path = os.path.join(lucas_data_path, 'subsequences_sample_{0}_n={1}_semistd{2}_std{3}_window{4}_step{5}.pickle'.format(lc_list_path, n, semi_standardize, standardize, window_size, step))
    clustering_threshold = 1
    not_weighted_str = ''
    if not weighted:
        not_weighted_str = '_notweighted'
    output_filename = 'sequence_tree_{0}_{1}samples_semistd{2}_std{3}_{4}levels{5}_{6}_{7}.dill'.format(lc_list_path, n,
                                                                                             semi_standardize, standardize,
                                                                                                max_level, not_weighted_str,
                                                                                                        window_size, step)
    output_full_path = os.path.join(output_path, output_filename)
    build_tree(sample_path, distances_path, db_path,
               output_full_path, max_level, clustering_threshold, weighted=weighted)


