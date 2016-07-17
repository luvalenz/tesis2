from subsequence_tree import SubsequenceTree
import pickle
import pandas as pd
from time_series import TimeSeriesOriginal, TimeSeriesSubsequence
import numpy as np
from scipy.spatial.distance import cdist


def get_macho_lightcurve(path):
    df = pd.read_csv(path, header=2, delimiter=' ')
    time = df['#MJD'].values
    magnitude = df['Mag'].values
    return TimeSeriesOriginal(time, magnitude, path)

if __name__ == '__main__':
    #root_path = '/home/lucas/Desktop/mackenzie_data/'
    root_path = '/user/luvalenz/mackenzie_data'
    #load affinities
    print("loading affinities")
    affinites_path = root_path + 'twed_matrix_t_w=250_num20000_macho.npz'
    npzfile = np.load(affinites_path)
    affinities = - npzfile[npzfile.files[0]]
    #load sample
    print("loading sample")
    sample_path = root_path + 'lcs_samples_t_w=250_num1000_macho.pickle'
    with open(sample_path, 'rb') as f:
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        sample = u.load()
    #build prototypes
    print("building prototypea")
    prototypes = [TimeSeriesSubsequence(time, magnitude, path, path)
                  for path, magnitude, time in zip(*sample)]
    max_level = 3
    print("building tree")
    st = SubsequenceTree(max_level, prototypes, affinities, [])
    st.save_graph()
    print(st.query_vector)
    test_ts = get_macho_lightcurve('/home/lucas/MACHO training lightcurves/BE/lc_1.3567.1310.B.mjd')
    result = st.make_query(test_ts)
    print("inverted_files")
    for node in st.node_shortcuts:
        print(node.inverted_file)
    print("query result")
    print(result)
    print("query vector")
    print(st.query_vector)
    print("d matrix")
    print(st.d_matrix)
    print("query result 2")
    print(cdist(np.matrix(st.query_vector), st.d_matrix)**2)