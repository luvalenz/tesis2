from time_series import TimeSeriesOriginal
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


def read_dataset(root):
    file_paths = glob.iglob(os.path.join(root, '**/*.*'))
    for path in file_paths:
        yield read_file(path)
