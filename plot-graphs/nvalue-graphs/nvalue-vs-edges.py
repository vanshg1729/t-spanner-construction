import sys
import os
from collections import defaultdict, OrderedDict
import json
import matplotlib.pyplot as plt
import numpy as np

def lower_bound_spanner_edges(n, t_value:int):
    k_value = (t_value + 1)/2
    return pow(n, 1 + 1/k_value)

def upper_bound_spanner_edges(n, t_value:int):
    k_value = (t_value + 1)/2
    return k_value * pow(n, 1 + 1/k_value)

def plot_expected_nvalue_vs_edges(ax, data):
    t_value = int(data['t_value'])
    no_of_tests = int(data['no_of_tests'])
    min_n_value = 3
    max_n_value = 3

    for i in range(no_of_tests):
        key = str(i)
        n_value = int(data[key]['n_value'])
        max_n_value = max(n_value, max_n_value)

    n_values = list(range(min_n_value, max_n_value + 1, 1))
    lower_bound = [lower_bound_spanner_edges(n_value, t_value) for n_value in n_values]
    upper_bound = [upper_bound_spanner_edges(n_value, t_value) for n_value in n_values]

    ax.plot(n_values, lower_bound, label='Lower bound of Spanner Edges')
    #ax.plot(n_values, upper_bound, label='Upper bound of Spanner Edges')

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
    data = plot_nvalue_vs_field('total_edges', ax, path)
    t_value = int(data['t_value'])

plot_expected_nvalue_vs_edges(ax, data)
ax.set_title(f"No of Nodes (N) vs Edges in t = {t_value} spanner (ms)")
ax.set_xlabel("N value")
ax.set_ylabel("Number of edges")

ax.legend()

plt.show()
