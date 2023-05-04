from collections import defaultdict
import json
import matplotlib.pyplot as plt

f = open('info.json')
data = json.load(f)
no_of_tests = int(data['no_of_tests'])
n_value = int(data['n_value'])
tests_per_t = int(data['tests_per_t'])
no_of_edges = defaultdict(int)

for i in range(no_of_tests):
    key = str(i)
    #print(f"key: {key}")
    t_value = data[key]['t_value'];
    total_edges = int(data[key]['total_edges'])
    no_of_edges[t_value] += total_edges

for key, value in no_of_edges.items():
    no_of_edges[key] = value/tests_per_t

fig, ax = plt.subplots()

ax.plot(no_of_edges.keys(), no_of_edges.values())
ax.set_title(f"T value vs Number of Spanner edges for {n_value} node graphs")
ax.set_xlabel("T value")
ax.set_ylabel("Number of edges in spanner graph")
plt.show()
