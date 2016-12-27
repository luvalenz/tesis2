import argparse
import sys
import time_series_utils
import glob2 as glob
import os
import random

def get_stratified_sample(dataset_dir, classes_df, n):
    classes = set(classes_df['class'])
    n_classes = len(classes)
    n_per_class = int(n/n_classes)
    sample = []
    for class_ in classes:
        filenames = classes_df[classes_df['class'] == class_]['filename'].tolist()
        class_sample = random.sample(filenames, n_per_class)
        sample += class_sample



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


if class_dict_path
lcs = [get_macho_lightcurve(path) for path in lcs_paths]


test_output = {'results': results, 'times': times}

with open(output_path, 'wb') as f:
        dill.dump(test_output, f)
