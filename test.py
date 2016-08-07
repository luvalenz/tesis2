import dill
import pandas as pd
from time_series import TimeSeriesOriginal
import os

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

if __name__ == '__main__':
    dataset_root = '/home/lucas/tesis2/macho_training_lightcurves/'
    #LOAD SUBSEQUENCE TREE
    st_path = '/home/lucas/tesis2/output/sequence_tree_20000samples_20levels_noNV.dill'
    with open(st_path, 'rb') as f:
        st = dill.load(f)
    #LOAD A MACHO LIGHTCURVE
    macho_lc_path = '/home/lucas/tesis2/macho_training_lightcurves/periodic/RRL/lc_1.3321.195.B.mjd'
    macho_lc = get_macho_lightcurve(macho_lc_path)
    query_result = st.make_query(macho_lc).sort([0])
    result_paths = query_result.index
    macho_lc.plot('blue')
    for path in result_paths:
        lc = get_macho_lightcurve(real_path(dataset_root, path))
        id_ = lc._id
        if 'RRL' in id_:
            print(id_)
        #lc.plot('black')

