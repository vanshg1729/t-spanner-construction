import sys
import os
from collections import defaultdict, OrderedDict
import json
import matplotlib.pyplot as plt
import numpy as np

def get_tvalue_vs_edges(field, data):
    no_of_tests = int(data['no_of_tests'])
    field_values = defaultdict(float)
    freq_t_value = defaultdict(int)

    # aggregating values over t-value
    for i in range(no_of_tests):
        key = str(i)
        t_value = int(data[key]['t_value'])
        if t_value % 2 == 0:
            t_value -= 1
        freq_t_value[t_value] += 1
        field_value = float(data[key][field])
        field_values[t_value] += field_value

    # averaging over all tests for each n-value
    for key, value in field_values.items():
        field_values[key] = value/freq_t_value[key]

    return field_values

paths = []
if len(sys.argv) > 2:
    paths = sys.argv[1:]
else:
    exit()

fig, ax = plt.subplots()

data = {}
n_value = 0

edge_dicts = []
data_dicts = []
impl_names = []

field = 'phase1_edge_count'

for path in paths:
    f = open(path)
    data = json.load(f)
    data_dicts.append(data)
    impl_names.append(os.path.basename(data['impl']))

    n_value = int(data['n_value'])
    field_values = get_tvalue_vs_edges(field, data)
    edge_dicts.append(field_values)

t_values = sorted(list(edge_dicts[0].keys()))
ratio_values = [edge_dicts[0][t]/edge_dicts[1][t] for t in t_values]

label = f'{field} ratio of {impl_names[0]} and {impl_names[1]}'

ax.plot(t_values, ratio_values, label=label)
ax.set_title(f"T value vs Ratio of Spanner Edges for {n_value} node graphs")
ax.set_xlabel("T value")
ax.set_ylabel("Ratio of edges")

ax.legend()

plt.show()
