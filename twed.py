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
    n_samples = int(sys.argv[1])
    #root = '/home/lucas/tesis2'
    # root = '/tmp/luvalenz'
    root = '/mnt/nas/GrimaRepo/luvalenz'
    input_path = os.path.join(root, 'lucas_data/subsequences_sample_n={0}.pickle'.format(n_samples))
    output_path = os.path.join(root, 'lucas_data/subsequences_distances_n={0}.npz'.format(n_samples))
    with open(input_path, 'rb') as f:
        subsequences = pickle.load(f)
    distmatrix = calculate_distances(subsequences)
    np.savez(output_path, distmatrix)