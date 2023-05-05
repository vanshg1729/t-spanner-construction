import sys
from collections import defaultdict
import json
import matplotlib.pyplot as plt
import numpy as np

path = ""
if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    exit()

f = open(path)
data = json.load(f)
no_of_tests = int(data['no_of_tests'])
n_value = int(data['n_value'])
tests_per_t = int(data['tests_per_t'])
spanner_time = defaultdict(float)
graph_edges = defaultdict(float)
max_t_value = 3

for i in range(no_of_tests):
    key = str(i)
    #print(f"key: {key}")
    t_value = data[key]['t_value']
    max_t_value = max(t_value, max_t_value)
    total_time = float(data[key]['total_time'])
    original_edges = int(data[key]['original_edges'])
    graph_edges[t_value] += original_edges
    spanner_time[t_value] += total_time

for key, value in spanner_time.items():
    spanner_time[key] = value/tests_per_t

for key, value in graph_edges.items():
    graph_edges[key] = value/tests_per_t

fig, ax = plt.subplots()

keys = list(spanner_time.keys())
program_time = list(spanner_time.values())
expected_time = [((t_value + 1)/2) * num_edges for t_value, num_edges in graph_edges.items()]

ax.plot(keys, program_time, label='Time to calculate T-spanner (ms)')
#ax.plot(keys, expected_time, label='Expected time to Construct the T-spanner')
ax.set_title(f"T value vs Time (ms) for {n_value} node graphs")
ax.set_xlabel("T value")
ax.set_ylabel("Time (ms)")
ax.legend()

plt.show()
