from time_series import TimeSeriesOriginal
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import numpy as np
import os
import glob2 as glob


def read_file(path):
    df = pd.read_csv(path, comment='#', sep=' ', header=None, skipinitialspace=True)
    not_nan_cols = np.where(~np.isnan(df.iloc[0]))[0]
    df = df[not_nan_cols]
    id_ = get_lightcurve_id(path)
    time = df.iloc[:, 0].values
    magnitude = df.iloc[:, 1].values
    not_nan = np.where(~np.logical_or(np.isnan(time), np.isnan(magnitude)))[0]
    time = time[not_nan]
    magnitude = magnitude[not_nan]
    ts = TimeSeriesOriginal(time, magnitude, id_)
    return ts


def read_files(paths):
    return (read_file(path) for path in paths)


def read_class_table(path):
    return pd.read_csv(path, sep=' ', index_col=0)


def stratified_sample(class_table, n_samples):
    X = class_table['path'].values
    y = class_table['class'].values
    sss = StratifiedShuffleSplit(n_splits=1, test_size=n_samples, random_state=0)
    for train_index, test_index in sss.split(X, y):
        return X[test_index].tolist()

def nonstratified_sample(paths_file_path, n):
    with open(paths_file_path) as f:
        num_lines = sum(1 for line in f)
    sample_indices = np.sort(np.random.choice(num_lines, n, replace=False))
    pointer = 0
    sample = []
    with open(paths_file_path) as f:
        for i, line in enumerate(f):
            if pointer == n:
                break
            if i == sample_indices[pointer]:
                sample.append(line[:-1])
                pointer += 1
    return sample


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
