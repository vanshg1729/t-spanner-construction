import sys
import os
from collections import defaultdict
import json
import matplotlib.pyplot as plt
import numpy as np

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
    #data = plot_tvalue_vs_field('spanner_max_path_len', ax, path)
    data = plot_tvalue_vs_field('spanner_avg_path_len', ax, path)
    n_value = int(data['n_value'])

ax.set_title(f"T value vs Graph Stats for {n_value} node graphs")
ax.set_xlabel("T value")
ax.set_ylabel("Spanner Edges")

ax.legend()

plt.show()
