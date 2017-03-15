import argparse
import sys
import os
import dill
import time_series_utils
import pandas as pd


parser = argparse.ArgumentParser(
    description='Build subsequence tree')
parser.add_argument('--results_path', required=True, type=str)
parser.add_argument('--output_dir', required=True, type=str)
parser.add_argument('--class_table_path', required=True, type=str)

args = parser.parse_args(sys.argv[1:])

class_table_path = args.class_table_path
results_path = args.results_path
output_dir = args.output_dir


print('reading class table...')
class_table = time_series_utils.read_class_table(class_table_path)
print('DONE')


print('reading results...')
with open(results_path, 'rb') as f:
    results = dill.load(f)
print('DONE')

target_ids = []
target_classes = []
ndcgs = []
times = []

print('Reordering results...')
for i, result in enumerate(results):
    print(i)
    target_id = result.target
    target_class, ndcg = result.ndcg(class_table)
    target_ids.append(target_id)
    target_classes.append(target_class)
    ndcgs.append(ndcg)
    times.append(result.times)
print('DONE')

ndcg_df = pd.DataFrame(ndcgs)
times_df = pd.DataFrame(times)

ndcg_df['id'] = target_ids
ndcg_df['class'] = target_classes

times_df['id'] = target_ids
times_df['class'] = target_classes

results_basename = os.path.splitext(os.path.basename(results_path))[0]

ndcg_basename = 'ndcg__{0}.csv'.format(results_basename)
times_basename = 'times__{0}.csv'.format(results_basename)
ndcg_output_path = os.path.join(output_dir, ndcg_basename)
times_output_path = os.path.join(output_dir, times_basename)

print('Writing files...')
ndcg_df.to_csv(ndcg_output_path)
times_df.to_csv(times_output_path)
print('DONE')

