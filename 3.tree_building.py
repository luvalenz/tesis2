import argparse
import sys
import os
import time_series_utils
from subsequence_tree import SubsequenceTree
import pickle
import dill

parser = argparse.ArgumentParser(
    description='Build subsequence tree')
parser.add_argument('--sample_dir', required=True, type=str)
parser.add_argument('--input_paths_file', default='', type=str)
parser.add_argument('--distances_dir', required=True, type=str)
parser.add_argument('--dataset_dir', default='', type=str)
parser.add_argument('--output_dir', required=True, type=str)
parser.add_argument('--dataset', required=True, type=str)
parser.add_argument('--n_samples', required=True, type=int)
parser.add_argument('--time_window', type=float, default=250)
parser.add_argument('--time_step', type=int, default=10)
parser.add_argument('--max_level', required=True, type=int)

args = parser.parse_args(sys.argv[1:])

sample_dir = args.sample_dir
input_paths_file = args.input_paths_file
distances_dir = args.distances_dir
dataset_dir = args.dataset_dir
output_dir = args.output_dir
dataset = args.dataset
n_samples = args.n_samples
time_window = args.time_window
time_step = args.time_step
max_level = args.max_level

sample_filename = 'sample_{0}_{1}_{2}_{3}.pkl'.format(dataset, n_samples,
                                                      time_window, time_step)
sample_path = os.path.join(sample_dir, sample_filename)
distances_filename = 'twed_{0}_{1}_{2}_{3}.pkl'.format(dataset, n_samples,
                                                       time_window, time_step)
distances_path = os.path.join(distances_dir, distances_filename)
output_filename = 'tree_{0}_{1}_{2}_{3}_{4}.dill'.format(dataset, n_samples,
                                                        time_window, time_step, max_level)
output_path = os.path.join(output_dir, output_filename)

with open(sample_path, 'rb') as f:
    sample = pickle.load(f)
with open(distances_path, 'rb') as f:
    distances_dict = pickle.load(f)

sample_ids = [subsequence.id for subsequence in sample]
distances_ids = distances_dict['ids']
if sample_ids == distances_ids:
    print('Sample file corresponds to distances file')
else:
    print('Sample file doesn\'t correspond to distances file')
    exit()

distances = distances_dict['distances']
affinities = -distances**2


if dataset_dir != '':
    dataset = time_series_utils.read_dataset(dataset_dir)
else:
    with open(input_paths_file, 'r') as f:
        lightcurves_paths = f.readlines()
    lightcurves_paths = (p[:-1] for p in lightcurves_paths if os.path.exists(p[:-1]))
    dataset = (time_series_utils.read_dataset(p) for p in lightcurves_paths)

print('building tree...')
tree = SubsequenceTree(max_level, sample, affinities, dataset, time_window, time_step)

with open( output_path, 'wb' ) as f:
    dill.dump(tree,  f)

print('DONE')

