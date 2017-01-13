import argparse
import sys
import time_series_utils
import dill
import numpy as np
import os


def query_nonlabeled_sample(paths_file_path, n):
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


def query_labeled_sample(classes_df, n_per_class):
    classes = set(classes_df['class'])
    sample = []
    for class_ in classes:
        paths = classes_df[classes_df['class'] == class_].index.tolist()
        try:
            class_sample = np.random.choice(paths, n_per_class, replace=False)
        except ValueError:
            class_sample = paths
        sample += list(class_sample)
    return sample


parser = argparse.ArgumentParser(
    description='Build subsequence tree')
parser.add_argument('--class_table_path', default='',  type=str)
parser.add_argument('--paths_list_path', default='',  type=str)
parser.add_argument('--n_queries', required=True, type=int)
parser.add_argument('--output_dir', required=True, type=str)
parser.add_argument('--name', required=True, type=str)

args = parser.parse_args(sys.argv[1:])


class_table_path = args.class_table_path
paths_list_path = args.paths_list_path
n_queries= args.n_queries
output_dir = args.output_dir
name = args.name


if class_table_path == '':
    paths = query_nonlabeled_sample(paths_list_path, n_queries)
    sample_type = 'nonlabeled'
else:
    class_table = time_series_utils.read_class_table(class_table_path)
    paths = query_labeled_sample(class_table, n_queries)
    sample_type = 'labeled'

lcs = time_series_utils.read_files(paths)

basename = 'querysample_{0}_{1}_{2}.dill'.format(name, sample_type, n_queries)
output_path = os.path.join(output_dir, basename)

with open(output_path, 'wb') as f:
    dill.dump(paths, f)
