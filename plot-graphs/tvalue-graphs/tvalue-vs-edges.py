import os
import sys
from collections import defaultdict
import json
import matplotlib.pyplot as plt
import numpy as np

def expected_spanner_edges(n, t_value:int):
    k_value = (t_value + 1)/2
    return k_value * pow(n, 1 + 1/k_value)

def plot_expected_tvalue_vs_edges(ax, data):
    n_value = int(data['n_value'])
    no_of_tests = int(data['no_of_tests'])
    max_t_value = 3

    for i in range(no_of_tests):
        key = str(i)
        t_value = data[key]['t_value']
        max_t_value = max(t_value, max_t_value)

    t_values = list(range(3, max_t_value + 1, 1))
    expected_edges = [expected_spanner_edges(n_value, t_value) for t_value in t_values]

    ax.plot(t_values, expected_edges, label='Expected Number of edges')


def plot_tvalue_vs_edges(ax, path):
    f = open(path)
    data = json.load(f)
    no_of_tests = int(data['no_of_tests'])
    tests_per_t = int(data['tests_per_t'])
    no_of_edges = defaultdict(int)

    impl_name = os.path.basename(data['impl'])

    for i in range(no_of_tests):
        key = str(i)
        #print(f"key: {key}")
        t_value = data[key]['t_value']
        total_edges = int(data[key]['total_edges'])
        no_of_edges[t_value] += total_edges

    for key, value in no_of_edges.items():
        no_of_edges[key] = value/tests_per_t

    keys = list(no_of_edges.keys())
    spanner_edges = list(no_of_edges.values())

    ax.plot(keys, spanner_edges, label=f'Spanner Edges using {impl_name}')
    return data

paths = []
if len(sys.argv) >= 2:
    paths = sys.argv[1:]
else:
    exit()

fig, ax = plt.subplots()

data = {}

for path in paths:
    data = plot_tvalue_vs_edges(ax, path)

#plot_expected_tvalue_vs_edges(ax, data)
n_value = int(data['n_value'])

ax.set_title(f"T value vs Number of Spanner edges for {n_value} node graphs")
ax.set_xlabel("T value")
ax.set_ylabel("Number of edges in spanner graph")
ax.legend()

plt.show()
