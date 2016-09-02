import numpy as np
import pandas as pd
from time_series import TimeSeriesOriginal
import pickle
import os
import sys


def get_macho_relative_path(path):
    start = path.find('macho_training_lightcurves')
    if start == -1:
        start = path.find('MACHO training lightcurves')
    path = path[start:]
    return path[path.find('/') + 1:]


def sample_lightcurves(paths_file_path, n_samples):
    with open(paths_file_path, 'r') as paths_file:
        paths = paths_file.readlines()
    return np.random.choice(paths, n_samples)


def get_macho_lightcurve(path):
    if path[-1] == '\n':
        path = path[:-1]
    df = pd.read_csv(path, header=2, delimiter=' ')
    time = df['#MJD'].values
    magnitude = df['Mag'].values
    return TimeSeriesOriginal(time, magnitude, get_macho_relative_path(path), True)


def sample_subsequences(root, paths_file_path, n_samples):
    subsequences = []
    paths = sample_lightcurves(paths_file_path, n_samples)
    paths = [os.path.join(root, path) for path in paths]
    lcs = (get_macho_lightcurve(path) for path in paths)
    for lc in lcs:
        subsequences += lc.get_random_subsequences(1)
    return subsequences



if __name__ == '__main__':
    input_path = sys.argv[1]
    n_samples = int(sys.argv[2])
    root = '/mnt/nas/GrimaRepo/luvalenz'
    root = '/home/lucas/tesis2'
    output_path = os.path.join(root,
                               'lucas_data/subsequences_sample_{0}_n={1}.pickle'.format(input_path,
                                                                                        n_samples))
    sample = sample_subsequences(root, input_path, n_samples)
    with open(output_path, 'wb') as f:
        pickle.dump(sample, f, protocol=2)