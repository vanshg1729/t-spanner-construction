#include <bits/stdc++.h>
#include <chrono>
using namespace std;

#define fr first
#define sc second
#define INF 1e9
typedef pair<int, int> pii;

const int maxn = 50000;

int choose_node(int n) {
    int x = rand() % n;
    int sqrt_n = sqrt(n);

    if (x <= sqrt_n) return 1;

    return 0;
}

int main() {

    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;

    set<pii> adj[maxn] = {}; // an adjacency list where we have a set for each node, storing pairs
    
    
    int cluster[maxn + 10] = {}; // tells the cluster to which node i belongs to
    vector<int> cluster_centers = {};
    int cluster_count = 0;

    vector<tuple<int, int, int>> spanner_edges = {};

    int n, m; cin >> n >> m;
    int sqrt_n = sqrt(n);
    int phase_one_edge_count = 0;
    int phase_two_edge_count = 0;
    int phase2_cluster_count = 0;

    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].insert({v, w});
        adj[v].insert({u, w});
    }

    auto phase1_start = high_resolution_clock::now();
    // Phase 1 : Cluster formation

    // choosing cluster center nodes randomly with (1/sqrt(n)) probability
    for (int i = 1; i <= n; i++) {
        if (choose_node(n)) {
            cluster[i] = i;
            cluster_count++;
            cluster_centers.push_back(i);
        }
    }

    // connecting non-sampled vertex to cluster centers
    for (int i = 1; i <= n; i++) {
        // continue if node is a cluster center
        if (cluster[i] == i) continue;

        int adjacent_cluster = false;
        int closest_cluster = 0;
        int cluster_dist = INF;

        // check if node is adjacent to any cluster center
        for (auto u : adj[i]) {
            if (cluster[u.fr] == u.fr) {
                adjacent_cluster = true;
                if (u.sc < cluster_dist) {
                    closest_cluster = u.fr;
                    cluster_dist = u.sc;
                }
            }
        }

        if (!adjacent_cluster) {
            // if node is not adjacent -> add all edges to spanner graph

            for (auto u : adj[i]) {
                spanner_edges.push_back({i, u.fr, u.sc});
                adj[u.fr].erase({i, u.sc});
            }

            adj[i].clear();
            continue;
        }
        
        // if node is adjacent to any cluster node -> add all edges <= cluster_dist
        vector<pii> added_edges = {};
        cluster[i] = closest_cluster;

        for (auto u : adj[i]) {
            if (u.sc <= cluster_dist) {
                added_edges.push_back(u);
                spanner_edges.push_back({i, u.fr, u.sc});
                adj[u.fr].erase({i, u.sc});
            }
        }

        for (auto u : added_edges) adj[i].erase(u);
    }
    
    // delete edges between non-sampled vertexes which belong to same cluster
    for (int i = 1; i <= n; i++) {
        if (cluster[i] == i) continue;

        vector<pii> delete_edges = {};

        for (auto u : adj[i]) {
            if (!(cluster[u.fr] == u.fr) && (cluster[u.fr] == cluster[i])) {
                adj[u.fr].erase({i, u.sc});
                delete_edges.push_back(u);
            }
        }

        for (auto edge : delete_edges) {
            adj[i].erase(edge);
        }
    }

    auto phase1_end = high_resolution_clock::now();
    phase_one_edge_count = spanner_edges.size();
    phase2_cluster_count = cluster_centers.size();

    // Phase 2 : Cluster-Vertex joining

    auto phase2_start = high_resolution_clock::now();
    for (int i = 1; i <= n; i++) {
        // smallest edge from i to all the clusters
        vector<pii> smallest_edge(n + 10, {0, INF});

        vector<pii> delete_edges = {}; // edges to be deleted from original graph

        for (auto u : adj[i]) {
            int cluster_center = cluster[u.fr];

            auto v = smallest_edge[cluster_center];

            if (u.sc < v.sc) {
                delete_edges.push_back(v);
                adj[v.fr].erase({i, v.sc});
                smallest_edge[cluster_center] = u;
            }
            else {
                delete_edges.push_back(u);
                adj[u.fr].erase({i, u.sc});
            }
        }

        for (auto u : delete_edges) adj[i].erase(u);

        for (auto u : adj[i]) {
            spanner_edges.push_back({i, u.fr, u.sc});
            adj[u.fr].erase({i, u.sc});
        }

        adj[i].clear(); // removing all the edges added to spanner graph
    }
    auto phase2_end = high_resolution_clock::now();

    int total_edges = spanner_edges.size();
    phase_two_edge_count = total_edges - phase_one_edge_count;

    cout << n << " " << total_edges << "\n";

    for (auto edge : spanner_edges) {
        cout << get<0>(edge) << " " << get<1>(edge) << " " << get<2>(edge) << "\n";
    }

    duration<double, std::milli> phase1_time = phase1_end - phase1_start;
    duration<double, std::milli> phase2_time = phase2_end - phase2_start;
    duration<double, std::milli> total_time = phase1_time + phase2_time;

    cout << phase_one_edge_count << "\n";
    cout << phase_two_edge_count << "\n";
    cout << phase1_time.count() << "\n";
    cout << phase2_time.count() << "\n";
    cout << total_time.count() << "\n";
    cout << phase2_cluster_count << "\n";
    /*
    cout << "Number of clusters: " << cluster_count << "\n";
    cout << "Phase 1 edge count: " << phase_one_edge_count << "\n";
    cout << "Phase 2 edge count: " << phase_two_edge_count << "\n";
    */
}
