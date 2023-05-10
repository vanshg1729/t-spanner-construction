import sys
import os
from collections import defaultdict
import json
import matplotlib.pyplot as plt
import numpy as np

def get_k_value(t_value):
    return (t_value + 1)/2

def plot_expected_tvalue_vs_complexity(ax, data):
    graph_edges = defaultdict(float)
    freq_t_value = defaultdict(int)
    no_of_tests = int(data['no_of_tests'])

    for i in range(no_of_tests):
        key = str(i)
        #print(f"key: {key}")
        t_value = int(data[key]['t_value'])
        original_edges = int(data[key]['original_edges'])
        if t_value % 2 == 0:
            t_value -= 1
        freq_t_value[t_value] += 1
        graph_edges[t_value] += original_edges

    for key, value in graph_edges.items():
        graph_edges[key] = value/freq_t_value[key]

    keys = list(graph_edges.keys())
    expected_time = [get_k_value(t_value) * num_edges for t_value, num_edges in graph_edges.items()]
    ax.plot(keys, expected_time, label='Expected time to Construct the T-spanner')

def plot_tvalue_vs_field(field, ax, path):
    f = open(path)
    data = json.load(f)
    no_of_tests = int(data['no_of_tests'])
    field_values = defaultdict(float)
    freq_t_value = defaultdict(int)

    impl_name = os.path.basename(data['impl'])

    # aggregating values over t-value
    for i in range(no_of_tests):
        key = str(i)

        t_value = int(data[key]['t_value'])
        if t_value % 2 == 0:
            t_value -= 1
        freq_t_value[t_value] += 1
        field_value = float(data[key][field])
        field_values[t_value] += field_value

    # averaging over all tests for each t-value
    for key, value in field_values.items():
        field_values[key] = value/freq_t_value[key]

    x_values = list(field_values.keys())
    y_values = list(field_values.values())

    is_time_field = True if ("time" in field) else False
    label = f'{field} using {impl_name}'
    if is_time_field:
        label += " (ms)"

    ax.plot(x_values, y_values, label=label)
    return data

paths = []
if len(sys.argv) >= 2:
    paths = sys.argv[1:]
else:
    exit()

fig, ax = plt.subplots()

n_value = 0
data = {}
for path in paths:
    data = plot_tvalue_vs_field('phase1_time', ax, path)
    plot_tvalue_vs_field('phase2_time', ax, path)
    #plot_tvalue_vs_field('total_time', ax, path)
    n_value = int(data['n_value'])

ax.set_title(f"T value vs Time (ms) for {n_value} node graphs")
ax.set_xlabel("T value")
ax.set_ylabel("Time (ms)")

ax.legend()

plt.show()
