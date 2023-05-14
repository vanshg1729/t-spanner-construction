import sys
import os
from collections import defaultdict, OrderedDict
import json
import matplotlib.pyplot as plt
import numpy as np

def get_nvalue_vs_edges(field, data):
    no_of_tests = int(data['no_of_tests'])
    field_values = defaultdict(float)
    edges = defaultdict(float)
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

    return field_values

paths = []
if len(sys.argv) > 2:
    paths = sys.argv[1:]
else:
    exit()

fig, ax = plt.subplots()

data = {}
t_value = 0

edge_dicts = []
data_dicts = []
impl_names = []

field = 'phase2_edge_count'

for path in paths:
    f = open(path)
    data = json.load(f)
    data_dicts.append(data)
    impl_names.append(os.path.basename(data['impl']))
    t_value = int(data['t_value'])
    field_values = get_nvalue_vs_edges(field, data)
    edge_dicts.append(field_values)

n_values = sorted(list(edge_dicts[0].keys()))
ratio_values = [edge_dicts[0][n]/edge_dicts[1][n] for n in n_values]

label = f'{field} ratio of {impl_names[0]} and {impl_names[1]}'

ax.plot(n_values, ratio_values, label=label)
ax.set_title(f"No of Nodes (N) vs Ratio of Spanner Edges in t = {t_value} spanner")
ax.set_xlabel("N value")
ax.set_ylabel("Ratio of Edges")

ax.legend()

plt.show()
