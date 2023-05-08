import sys
import os
from collections import defaultdict, OrderedDict
import json
import matplotlib.pyplot as plt
import numpy as np

def plot_expected_nvalue_vs_complexity(ax, data):
    graph_edges = defaultdict(float)
    no_of_tests = int(data['no_of_tests'])
    tests_per_n = int(data['tests_per_n'])
    t_value = int(data['t_value'])

    for i in range(no_of_tests):
        key = str(i)
        #print(f"key: {key}")
        n_value = int(data[key]['n_value'])
        original_edges = int(data[key]['original_edges'])
        graph_edges[n_value] += original_edges

    for key, value in graph_edges.items():
        graph_edges[key] = value/tests_per_n

    n_values = sorted(list(graph_edges.keys()))
    expected_time = [((t_value + 1)/2) * graph_edges[n] for n in n_values]
    ax.plot(n_values, expected_time, label=f'Expected time to Construct T = {t_value} spanner')

def plot_nvalue_vs_field(field, ax, path):
    f = open(path)
    data = json.load(f)
    no_of_tests = int(data['no_of_tests'])
    tests_per_n = int(data['tests_per_n'])
    field_values = defaultdict(float)

    impl_name = os.path.basename(data['impl'])

    # aggregating values over t-value
    for i in range(no_of_tests):
        key = str(i)
        n_value = int(data[key]['n_value'])
        field_value = float(data[key][field])
        field_values[n_value] += field_value

    # averaging over all tests for each t-value
    for key, value in field_values.items():
        field_values[key] = value/tests_per_n

    x_values = sorted(list(field_values.keys()))
    y_values = [field_values[x] for x in x_values]

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

data = {}
t_value = 0
for path in paths:
    data = plot_nvalue_vs_field('total_time', ax, path)
    t_value = int(data['t_value'])

#plot_expected_nvalue_vs_complexity(ax, data)
ax.set_title(f"No of Nodes (N) vs Time to create t = {t_value} spanner (ms)")
ax.set_xlabel("N value")
ax.set_ylabel("Time (ms)")

ax.legend()

plt.show()
