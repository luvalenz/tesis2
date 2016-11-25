from time_series import TimeSeriesOriginal
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import numpy as np
import os
import glob2 as glob



def read_file(path):
    df = pd.read_csv(path, comment='#', sep=' ', header=None)
    not_nan_cols = np.where(~np.isnan(df.iloc[0]))[0]
    df = df[not_nan_cols]
    id_ = os.path.basename(path)
    time = df.iloc[:, 0].values
    magnitude = df.iloc[:, 1].values
    not_nan = np.where(~np.logical_or(np.isnan(time), np.isnan(magnitude)))[0]
    ts = TimeSeriesOriginal(time[not_nan], magnitude[not_nan], id_)
    return ts


def read_class_table(path):
    return pd.read_csv(path, sep=' ', index_col=0)


def stratified_sample(class_file_path, paths):
    table = read_class_table(class_file_path)
    add_paths_to_class_table(table, paths)
    table = table[table['path'] != 0]
    X = table['path'].values
    y = table['class'].values
    sss = StratifiedShuffleSplit(n_splits=1, test_size=20000, random_state=0)
    for train_index, test_index in sss.split(X, y):
        return X[test_index].tolist()


def get_lightcurve_id(fp):
    basename = os.path.basename(fp)
    filename = '.'.join(basename.split('.')[:-1])
    if filename.startswith('lc_'):
        filename = filename[3:]
    if filename.endswith('.B') or filename.endswith('.R'):
        filename = filename[:-2]
    return filename


def add_paths_to_class_table(class_table, paths):
    index = class_table.index
    class_table['path'] = pd.Series(np.zeros_like(index.values), index=index)
    for p in paths:
        id_ = get_lightcurve_id(p)
        if id_ in class_table.index:
            class_table.loc[id_, 'path'] = p


def read_dataset(root):
    file_paths = glob.iglob(os.path.join(root, '**/*.*'))
    for path in file_paths:
        yield read_file(path)
