import numpy as np
from sklearn.cluster import AffinityPropagation
#import matplotlib.pyplot as plt


def get_distance_matrix(file_path):
    npz = np.load(file_path)
    return npz[npz.files[0]]


def run_affinity_propagation(affinities, preference_factor):
    min_af = np.min(affinities)
    max_af= np.max(affinities)
    range_af = max_af-min_af
    af = AffinityPropagation(preference=min_af-preference_factor*range_af)
    af.fit(affinities)
    cluster_centers_indices = af.cluster_centers_indices_
    n_clusters_ = len(cluster_centers_indices)
    return n_clusters_


def run_validation(affinities):
    x = np.exp(np.arange(10))
    y = np.array([run_affinity_propagation(affinities, preference_factor)
                  for preference_factor in x])
    indices = np.where(x >= len(affinities))[0]
    reg = np.polyfit(np.log(x[indices]), np.log(y[indices]), 1)
    return x, y, reg

if __name__ == '__main__':
    matrix_path = '/user/luvalenz/mackenzie_data/twed_matrix_t_w=250_num20000_macho.npz'
    distances = get_distance_matrix(matrix_path)
    affinities = -distances
    print("running validation...")
    x, y, reg = run_validation(affinities)
    print("DONE")
    m, n = reg
    print(m, n)





