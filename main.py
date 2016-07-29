from subsequence_tree import SubsequenceTree
import pickle
import dill
import pandas as pd
from time_series import TimeSeriesOriginal, TimeSeriesSubsequence
import numpy as np
import glob2 as glob
import os


def get_macho_dataset(root, max_files=None):
    paths = glob.iglob(os.path.join(root, '**/*.mjd'))
    if max_files is not None:
        paths = list(paths)[:max_files]
    lightcurves = (get_macho_lightcurve(file_path)
                   for file_path in  paths)
    return lightcurves


def get_macho_lightcurve(path):
    df = pd.read_csv(path, header=2, delimiter=' ')
    print(path)
    time = df['#MJD'].values
    magnitude = df['Mag'].values
    return TimeSeriesOriginal(time, magnitude, path)

def results_are_equal(r1, r2):
    r1 = r1.values
    r2 = r2.values
    return np.all(r1 - r2 < 1e-3)


def build_tree(sample_path, affinities_path, db_path,
               output_path, max_level, clustering_threshold):
    with open(sample_path, 'rb') as f:
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        sample = u.load()
    prototypes = [TimeSeriesSubsequence(time, magnitude, path, path)
                  for path, magnitude, time in zip(*sample)]
    npzfile = np.load(affinities_path)
    distances = npzfile[npzfile.files[0]]
    affinities = - distances
    dataset = get_macho_dataset(db_path)
    print('building tree...')
    st = SubsequenceTree(max_level, prototypes, affinities, dataset, max_level, clustering_threshold)
    print('done')
    with open( output_path, "wb" ) as f:
        dill.dump(st,  f)


if __name__ == '__main__':
    #root_path = '/home/lucas/tesis2'
    root_path = '/tmp/luvalenz'
    mac_data_path = os.path.join(root_path, 'mackenzie_data/')
    db_path = os.path.join(root_path, 'macho_training_lightcurves')
    output_path = os.path.join(root_path, 'output')
    n = 20000
    affinities_path = os.path.join(mac_data_path, 'twed_matrix_t_w=250_num{0}_macho.npz'.format(n))
    sample_path = os.path.join(mac_data_path, 'lcs_samples_t_w=250_num{0}_macho.pickle'.format(n))
    max_level = 1000
    clustering_threshold = 10
    output_filename = 'sequence_tree_{0}samples_{1}levels.dill'.format(n, max_level)
    output_full_path = os.path.join(output_path, output_filename)
    build_tree(sample_path, affinities_path, db_path,
               output_full_path, max_level, clustering_threshold)




