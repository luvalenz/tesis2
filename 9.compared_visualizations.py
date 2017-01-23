import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import pickle

def plot_times(times, names, y_label, plot_title, path):
    plt.clf()
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.boxplot(times, showmeans=True)
    plt.xticks(list(range(len(names))), names, rotation=45)
    plt.ylabel(y_label)
    plt.title(plot_title)
    plt.savefig(path)

parser = argparse.ArgumentParser(
    description='Build subsequence tree')
parser.add_argument('--results_paths', required=True, type=str)
parser.add_argument('--times_paths', required=True, type=str)
parser.add_argument('--names', required=True, type=str)
parser.add_argument('--output_dir', required=True, type=str)

args = parser.parse_args(sys.argv[1:])

results_paths = args.results_paths.split(',')
times_paths = args.times_paths.split(',')
names = args.names.split(',')
output_dir = args.output_dir

if not(len(times_paths) == len(results_paths) == len(names)):
    exit(-1)

result_dfs = (pd.read_csv(rp, index_col=0) for rp in results_paths)
time_dfs = (pd.read_csv(tp, index_col=0) for tp in times_paths)

total_times = [times.drop(['id', 'class'], axis=1).values.sum(axis=1).tolist()
               for times in time_dfs]


