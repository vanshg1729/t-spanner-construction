import sys
import os
from collections import defaultdict, OrderedDict
import json
import matplotlib.pyplot as plt
import numpy as np

def plot_nvalue_vs_field(field, ax, path):
    f = open(path)
    data = json.load(f)
    no_of_tests = int(data['no_of_tests'])
    field_values = defaultdict(float)
    freq_n_value = defaultdict(int)

    impl_name = os.path.basename(data['impl'])

    # aggregating values over n-value
    for i in range(no_of_tests):
        key = str(i)
        n_value = int(data[key]['n_value'])
        freq_n_value[n_value] += 1
        field_value = float(data[key][field])
        field_values[n_value] += field_value

    # averaging over all tests for each n-value
    for key, value in field_values.items():
        field_values[key] = value/freq_n_value[key]

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
    data = plot_nvalue_vs_field('phase2_cluster_count', ax, path)
    t_value = int(data['t_value'])

ax.set_title(f"No of Nodes (N) vs cluster count for t = {t_value} spanner")
ax.set_xlabel("N value")
ax.set_ylabel("Number of Clusters after Phase 1")

ax.legend()

plt.show()
