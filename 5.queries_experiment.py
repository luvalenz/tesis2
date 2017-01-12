import argparse
import sys
import time_series_utils
import glob2 as glob
import os
import random


def get_non_stratified_sample(dataset_dir, n):
    paths = list(glob.iglob(os.path.join(dataset_dir, '**/*')))
    return random.sample(paths, n)


parser = argparse.ArgumentParser(
    description='Build subsequence tree')
parser.add_argument('--tree_dir', required=True, type=str)
parser.add_argument('--dataset_dir', required=True, type=str)
parser.add_argument('--output_dir', required=True, type=str)
parser.add_argument('--class_dict_path', default='',  type=str)
parser.add_argument('--n_queries', required=True, type=int)

args = parser.parse_args(sys.argv[1:])

tree_dir = args.tree_dir
dataset_dir = args.dataset_dir
output_dir = args.output_dir
class_dict_path = args.class_dict_path
n_queries= args.n_queries


if class_dict_path == '':
    lcs = get_non_stratified_sample(dataset_dir, n_queries)
else:
    lcs = time_series_utils.stratified_sample(dataset_dir, classes_df, n_queries)



test_output = {'results': results, 'times': times}

with open(output_path, 'wb') as f:
        dill.dump(test_output, f)
