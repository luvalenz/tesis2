import argparse
import sys
import os
import time_series_utils
from subsequence_tree import SubsequenceTree
from subsequence_tree_2 import BottomUpSubsequenceTree
import pickle
import dill

parser = argparse.ArgumentParser(
    description='Build subsequence tree')
parser.add_argument('--sample_dir', required=True, type=str)
parser.add_argument('--input_paths_file', default='', type=str)
parser.add_argument('--distances_dir', required=True, type=str)
parser.add_argument('--dataset_root', default='', type=str)
parser.add_argument('--output_dir', required=True, type=str)
parser.add_argument('--dataset', required=True, type=str)
parser.add_argument('--n_samples', required=True, type=int)
parser.add_argument('--time_window', type=float, default=250)
parser.add_argument('--time_step', type=int, default=10)
parser.add_argument('--max_level', required=True, type=int)
parser.add_argument('--class_table_path', default='', type=str)
parser.add_argument('--tree_type', default=0, type=int)

args = parser.parse_args(sys.argv[1:])

sample_dir = args.sample_dir
input_paths_file = args.input_paths_file

distances_dir = args.distances_dir
dataset_root = args.dataset_root
output_dir = args.output_dir
dataset = args.dataset
n_samples = args.n_samples
time_window = args.time_window
time_step = args.time_step
max_level = args.max_level
class_table_path = args.class_table_path
tree_type = args.tree_type

approach = 'topdown'
if tree_type == 2:
    approach = 'bottomup'

sample_filename = 'sample_{0}_{1}_{2}_{3}.pkl'.format(dataset, n_samples,
                                                      time_window, time_step)
sample_path = os.path.join(sample_dir, sample_filename)
distances_filename = 'twed_{0}_{1}_{2}_{3}.pkl'.format(dataset, n_samples,
                                                       time_window, time_step)
distances_path = os.path.join(distances_dir, distances_filename)
output_filename = 'tree_{0}_{1}_{2}_{3}_{4}_{5}.dill'.format(dataset, n_samples,
                                                        time_window, time_step, max_level,
                                                        approach)
output_path = os.path.join(output_dir, output_filename)

print('Opening samples file...')
with open(sample_path, 'rb') as f:
    sample = pickle.load(f)
print('DONE')
print('Opening distances file...')
with open(distances_path, 'rb') as f:
    distances_dict = pickle.load(f)
print('DONE')

print('Checking file correctnesss...')
sample_ids = [subsequence.id for subsequence in sample]
distances_ids = distances_dict['ids']
if sample_ids == distances_ids:
    print('Sample file corresponds to distances file')
else:
    print('Sample file doesn\'t correspond to distances file')
    exit()
print('DONE')

distances = distances_dict['distances']
affinities = -distances



if input_paths_file != '':
    print('Reading file paths')
    with open(input_paths_file, 'r') as f:
        lightcurves_paths = f.readlines()
    print('DONE')
    print('Reading dataset...')
    lightcurves_paths = (os.path.join(dataset_root, p[:-1]) for p in lightcurves_paths if os.path.exists(p[:-1]))
    dataset = (time_series_utils.read_file(p) for p in lightcurves_paths)
    print('DONE')
elif class_table_path  != '':
    print('Reading dataset...')
    class_table = time_series_utils.read_class_table(class_table_path)
    lightcurves_paths = class_table['path'].values
    lightcurves_paths = (os.path.join(dataset_root, p) for p in lightcurves_paths)
    dataset = (time_series_utils.read_file(p) for p in lightcurves_paths)
    print('DONE')
else:
    print('Reading dataset...')
    dataset = time_series_utils.read_dataset(dataset_root)
    print('DONE')

dataset = (lc for lc in dataset if lc.total_time >= time_window)

print('Building tree...')
if tree_type == 2:
    print('BOTTOM UP APPROACH')
    tree = BottomUpSubsequenceTree(max_level, sample, affinities,
                                   dataset, time_window, time_step)
else:
    print('TOP DOWN APPROACH')
    tree = SubsequenceTree(max_level, sample, affinities,
                           dataset, time_window, time_step)
print('DONE')

print('Saving tree...')
with open( output_path, 'wb') as f:
    dill.dump(tree,  f)
print('DONE')

