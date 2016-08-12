import dill
import pandas as pd
from time_series import TimeSeriesOriginal
import os
import matplotlib.pyplot as plt

def get_macho_class_from_path(path):
    classes = ['BE', 'ML', 'NV', 'QSO', 'CEPH', 'EB', 'LPV', 'RRL']
    for c in classes:
        if c in path:
            return c
    return None

def real_path(root, path):
    start = path.find('macho_training_lightcurves')
    if start != -1:
        path = path[start:]
        path = path[path.find('/') + 1:]
    full_path = os.path.join(root, path)
    return full_path

def get_macho_lightcurve(path):
    df = pd.read_csv(path, header=2, delimiter=' ')
    time = df['#MJD'].values
    magnitude = df['Mag'].values
    return TimeSeriesOriginal(time, magnitude, path)

def plot_lc(lc, color='blue'):
    time = lc.time
    mag = lc.magnitude
    plt.clf()
    plt.plot(time, mag, '.', color=color)
    plt.show()

if __name__ == '__main__':
    dataset_root = '/home/lucas/tesis2/macho_training_lightcurves/'
    #LOAD SUBSEQUENCE TREE
    st_path = '/home/lucas/tesis2/output/sequence_tree_1000samples_20levels_noNV.dill'
    with open(st_path, 'rb') as f:
        st = dill.load(f)
    #LOAD A MACHO LIGHTCURVE
    macho_lc_path = '/home/lucas/tesis2/macho_training_lightcurves/periodic/RRL/lc_1.4046.937.R.mjd'
    #macho_lc_path = '/home/lucas/tesis2/macho_training_lightcurves/BE/lc_1.3567.1310.B.mjd'
    #macho_lc_path = '/home/lucas/tesis2/macho_training_lightcurves/periodic/CEPH/lc_1.3441.15.B.mjd'
    macho_lc = get_macho_lightcurve(macho_lc_path)
   # plot_lc(macho_lc, 'red')
    query_result = st.make_query(macho_lc)
    query_result = query_result.sort([0])
    result_paths = query_result.index
    print(query_result)
    for path in result_paths:
        lc = get_macho_lightcurve(real_path(dataset_root, path))
      #  plot_lc(lc)
        #lc.plot('black')

