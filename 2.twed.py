from scipy.spatial.distance import pdist, squareform
import itertools
from distance_utils import time_series_twed
import pickle
import numpy as np
import os
import sys

def calculate_distances(subsequences):
    distances = [time_series_twed(i, j) for i, j in itertools.combinations(subsequences, 2)]
    return squareform(distances)



if __name__ == '__main__':
    lc_list_path = sys.argv[1]
    n_samples = int(sys.argv[2])
    semi_standardize = False
    standardize = False
    if len(sys.argv) > 3:
        if sys.argv[3] == 'semi':
            semi_standardize = True
            print('semi standarized')
        if sys.argv[3] == 'std':
            standardize = True
            print('standarized')
    root = '/mnt/nas/GrimaRepo/luvalenz'
    input_path = 'lucas_data/subsequences_sample_{0}_n={1}_semistd{2}_std{3}.pickle'
    input_path = os.path.join(root, input_path.format(lc_list_path, n_samples, semi_standardize, standardize))
    output_path = 'lucas_data/subsequences_distances_{0}_n={1}_semistd{2}_std{3}.npz'
    output_path = os.path.join(root, output_path.format(lc_list_path, n_samples, semi_standardize, standardize))
    with open(input_path, 'rb') as f:
        subsequences = pickle.load(f)
    distmatrix = calculate_distances(subsequences)
    np.savez(output_path, distmatrix)