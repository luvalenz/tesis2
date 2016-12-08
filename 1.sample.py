import argparse
import sys
import os
import glob2 as glob
import random
import pickle
import time_series_utils



parser = argparse.ArgumentParser(
    description='Get samples from lightcurves.')
parser.add_argument('--input_dir', default='', type=str)
parser.add_argument('--input_paths_file', default='', type=str)
parser.add_argument('--class_file', default='', type=str)
parser.add_argument('--output_dir', required=True, type=str)
parser.add_argument('--dataset', required=True, type=str)
parser.add_argument('--n_samples', required=True, type=int)
parser.add_argument('--time_window', type=float, default=250)
parser.add_argument('--time_step', type=int, default=10)

args = parser.parse_args(sys.argv[1:])

input_dir = args.input_dir
input_paths_file = args.input_paths_file
class_file = args.class_file
output_dir = args.output_dir
dataset = args.dataset
n_samples = args.n_samples
time_window = args.time_window
time_step = args.time_step

output_filename = 'sample_{0}_{1}_{2}_{3}.pkl'.format(dataset, n_samples,
                                                      time_window, time_step)
output_path = os.path.join(output_dir, output_filename)

print('getting paths...')
if input_dir != '':
    lightcurves_paths = list(glob.iglob(os.path.join(input_dir, '**/*')))
else:
    with open(input_paths_file, 'r') as f:
        #lightcurves_paths = f.readlines()
        lightcurves_paths = []
        for i in range(20001):
            lightcurves_paths.append(f.readline())
    lightcurves_paths = [p[:-1] for p in lightcurves_paths if os.path.exists(p[:-1])]
print('DONE')

# print('Sampling lightcurves...')
# if class_file == '':
#     lightcurves_paths_sample = random.sample(lightcurves_paths, n_samples)
# else:
#     lightcurves_paths_sample = time_series_utils.stratified_sample(class_file, lightcurves_paths, n_samples)
#
# print('DONE')

lightcurves_paths_sample = lightcurves_paths
print('Opening lightcurves...')
lightcurves_sample = (time_series_utils.read_file(path) for path in lightcurves_paths_sample)
print('DONE')

print('Getting subsequences...')
subsequences_sample = [lc.get_random_subsequence(time_window)
                       for lc in lightcurves_sample]
print('DONE')

with open(output_path, 'wb') as f:
    pickle.dump(subsequences_sample, f, protocol=2)





