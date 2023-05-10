/*
Run Instructions : ./a.out <t-value> < <infile>
* implementation of paper :
* A Simple and Linear Time Randomized Algorithm for
Computing Sparse Spanners in Weighted Graphs
* By - Surender Baswana, Sandeep Sen
* Link : https://www.cse.iitd.ac.in/~ssen/journals/randstruc.pdf

*/

#include <bits/stdc++.h>
#include <chrono>
using namespace std;

#define fr first
#define sc second
#define INF 1e9
typedef pair<int, int> pii;

const int maxn = 50000;

typedef struct node{
    list<struct node>::iterator sibling;
    int v;
    int w;
} Node;

Node createNode(int v, int w, list<struct node>::iterator sibling){
    Node n;
    n.v = v;
    n.w = w;
    n.sibling = sibling;
    return n;
}


int choose_node(int n, int k) {
    double exponent = (1.0 -1.0/k);
    int x = rand() % n;
    double num = pow(n, exponent);

    if ((double) x <= num) return 1;

    return 0;
}

int main(int argc, char *argv[]) {

    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;

    int t = 3; // t-value for t-spanner
    if (argc > 1) {
        t = atoi(argv[1]);
        //cout << "value of k: " << k << "\n";
    }
    int k = (int)((t + 1)/2.0);

    // set<pii> adj[maxn] = {};
    // LLL
    list<Node> adjl[maxn];

    int cluster[maxn + 10] = {}; // tells the cluster to which node i belongs to
    int is_cluster[maxn + 10] = {}; // tells whether a node is a cluster center
    vector<int> cluster_centers[2] = {};
    vector<tuple<int, int, int>> cluster_edges[2] = {};
    int cluster_count = 0;
    int phase_one_edge_count = 0;
    int phase_two_edge_count = 0;
    int phase2_cluster_count = 0;

    vector<tuple<int, int, int>> spanner_edges = {};

    int n, m; cin >> n >> m;

    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        // adj[u].insert({v, w});
        // adj[v].insert({u, w});

        // LLL
        Node n1 = createNode(v, w, adjl[v].begin());
        Node n2 = createNode(u, w, adjl[u].begin());
        list<Node>::iterator it1 = adjl[u].insert(adjl[u].end(), n1);
        list<Node>::iterator it2 = adjl[v].insert(adjl[v].end(), n2);
        it1->sibling = it2;
        it2->sibling = it1;
    }

    auto phase1_start = high_resolution_clock::now();
    // Phase 1: Cluster formation

    // initializing C_0
    for (int i = 1; i <= n; i++) {
        cluster[i] = i;
        cluster_centers[0].push_back(i);
    }

    int iter;
    for (iter = 1; iter < k; iter++) {
        int idx = iter % 2;
        int p_idx = (iter + 1) % 2;

        // E_i : edges belonging to cluster
        // C_i : cluster centers
        // initialing C_i and E_i
        memset(is_cluster, 0, maxn * sizeof(int));
        cluster_centers[idx].clear();
        cluster_edges[idx].clear();
        
        // Start of Step 1: Forming a sample of Clusters

        // sampling the cluster centers with probability (n^(-1/k))
        for (auto u : cluster_centers[p_idx]) {
            if (choose_node(n, k)) {
                is_cluster[u] = 1;
                cluster_centers[idx].push_back(u);
            }
        }

        // adding cluster edges from (E_(i-1)) to E_i
        for (auto edge : cluster_edges[p_idx]) {
            int u = get<0>(edge), v = get<1>(edge); 
            int w = get<2>(edge);
            if (is_cluster[u]) {
                cluster[v] = u;
                cluster_edges[idx].push_back(edge);
            }
            else if (is_cluster[v]) {
                cluster[u] = v;
                cluster_edges[idx].push_back(edge);
            }
        }
        // End of Step 1
        
        // Start of Step 2: Finding nearest neighboring sampled cluster for each vertex

        // finding closter cluster neighbor for each node that
        // does not belong to any sampled cluster
        for (int i = 1; i <= n; i++) {
            // if parent cluster of i is sampled cluster -> continue
            if (is_cluster[cluster[i]]) continue;

            int adjacent_cluster = false;
            int closest_cluster = 0;
            list<Node>::iterator closest_cluster_iterator = adjl[i].begin();
            int cluster_dist = INF;
            pii closest_edge = {};

            // check if node is adjacent to any cluster center
            // for (auto u : adj[i]) {
            //     if (is_cluster[cluster[u.fr]]) {
            //         adjacent_cluster = true;
            //         if (u.sc < cluster_dist) {
            //             closest_cluster = cluster[u.fr];
            //             cluster_dist = u.sc;
            //             closest_edge = u;
            //         }
            //     }
            // }
            
            // LLL
            
            // check if node is adjacent to any cluster center
            for (list<Node>::iterator it = adjl[i].begin(); it != adjl[i].end(); it++) {
                if (is_cluster[cluster[it->v]]) {
                    adjacent_cluster = true;
                    // cout<<"adjacent"<<endl;
                    if (it->w < cluster_dist) {
                        closest_cluster = cluster[it->v];
                        cluster_dist = it->w;
                        closest_edge = {it->v, it->w};
                        closest_cluster_iterator = it;
                    }
                }
            }

            // End of Step 2

            // Start of Step 3: Adding edges to spanner

            // if node is not adjacent to any sampled cluster,
            // then add smallest edge from node to all the old non-sampled
            // clusters (Phase 1 - 3(a))
            if (!adjacent_cluster) {
                // smallest edge from i to all the old clusters
                // vector<pii> smallest_edge(n + 10, {0, INF});

                // vector<pii> delete_edges = {}; // edges to be deleted from original graph

                // for (auto u : adj[i]) {
                //     int cluster_center = cluster[u.fr];
                //     if (is_cluster[cluster_center]) {
                //         cout << "Something is wrong, this should not happen\n";
                //         continue;
                //     }

                //     auto v = smallest_edge[cluster_center];

                //     if (u.sc < v.sc) {
                //         delete_edges.push_back(v);
                //         adj[v.fr].erase({i, v.sc});
                //         smallest_edge[cluster_center] = u;
                //     }
                //     else {
                //         delete_edges.push_back(u);
                //         adj[u.fr].erase({i, u.sc});
                //     }
                // }

                // for (auto u : delete_edges) adj[i].erase(u);

                // for (auto u : adj[i]) {
                //     spanner_edges.push_back({i, u.fr, u.sc});
                //     adj[u.fr].erase({i, u.sc});
                // }

                // adj[i].clear(); // removing all the edges added to spanner graph
                
                // LLL

                vector<list<Node>::iterator> smallest_edge_iterators(n + 10, adjl[i].end());

                //  Remove nodes larger than the smallest
                for(list<Node>::iterator it = adjl[i].begin(); it != adjl[i].end();){
                    int cluster_center = cluster[it->v];
                    if (is_cluster[cluster_center]) {
                        cout << "#Something is wrong, this should not happen\n";
                        continue;
                    }
                    auto sm = smallest_edge_iterators[cluster_center];

                    if (sm == adjl[i].end() || it->w < sm->w) {
                        // delete_edges.push_back(v);
                        if(sm != adjl[i].end()){
                            adjl[sm->v].erase(sm->sibling);
                            adjl[i].erase(sm);
                        }

                        smallest_edge_iterators[cluster_center] = it;
                        it++;
                    }
                    else {
                        // delete_edges.push_back({it->v, it->w});
                        adjl[it->v].erase(it->sibling);
                        it = adjl[i].erase(it);
                    }
                }

                // add smallest to spanner and remove from adjl
                for(list<Node>::iterator it = adjl[i].begin(); it != adjl[i].end();){
                    spanner_edges.push_back({i, it->v, it->w});
                    adjl[it->v].erase(it->sibling);
                    it = adjl[i].erase(it);
                }
                
                continue;
            }

            // node is adjacent to a sampled cluster (Phase 1 - 3(b))
            // add this edge, add any other edge which is less than this edge

            // adding the smallest edge to a neighboring sampled cluster
            // to spanner_edges (E_S) and cluster_edges (E_i)
            auto e = closest_edge;
            cluster[i] = closest_cluster;
            assert(closest_cluster > 0);
            // cout<<closest_edge.fr<<" "<<closest_edge.sc<<endl;
            spanner_edges.push_back({i, e.fr, e.sc});
            cluster_edges[idx].push_back({i, e.fr, e.sc});
            
            // removing this edge from original graph
            // adj[i].erase(e);
            // adj[e.fr].erase({i, e.sc});
            // LLL
            adjl[e.fr].erase(closest_cluster_iterator->sibling);
            adjl[i].erase(closest_cluster_iterator);


            // smallest edge from i to all the old clusters
            vector<pii> smallest_edge(n + 10, {0, INF});

            // mark all the cluster centers (old and new) to which
            // node i has an edge whose weight is less than weight
            // of closest edge
            vector<int> mark_center(n + 10, 0);
            mark_center[closest_cluster] = 1;

            // vector<pii> delete_edges = {};

            // // finding smallest edge from node i to all clusters (old and new)
            // for (auto u : adj[i]) {
            //     int cluster_center = cluster[u.fr];
            //     if (is_cluster[cluster_center]) {
            //             cout << "Something is wrong, this should not happen\n";
            //             continue;
            //     }
            //     auto v = smallest_edge[cluster_center];

            //     if (u.sc < v.sc) {
            //         smallest_edge[cluster_center] = u;
            //         if (u.sc <= closest_edge.sc) {
            //             mark_center[cluster_center] = 1;
            //         }
            //     }
            // }

            // LLL

            for (auto u : adjl[i]) {
                int cluster_center = cluster[u.v];
                // if (is_cluster[cluster_center]) {
                //         cout << "Something is wrong, this should not happen\n";
                //         continue;
                // }
                auto v = smallest_edge[cluster_center];

                if (u.w < v.sc) {
                    smallest_edge[cluster_center] = {u.v, u.w};
                    if (u.w <= closest_edge.sc) {
                        mark_center[cluster_center] = 1;
                    }
                }
            }
            
            // -------------
            // adding the least weight edges from each cluster to
            // spanner graph
            vector<int> seen(n + 10, 0);
            // for (auto u : adj[i]) {
            //     int cluster_center = cluster[u.fr];

            //     auto v = smallest_edge[cluster_center];

            //     if (mark_center[cluster_center]) {
            //         if (!seen[cluster_center]) {
            //             spanner_edges.push_back({i, v.fr, v.sc});
            //             seen[cluster_center] = 1;
            //         }
            //         delete_edges.push_back(u);
            //         adj[u.fr].erase({i, u.sc});
            //     }
            // }

            // // delete non-smallest edges from all the clusters connected to i
            // for (auto edge : delete_edges) adj[i].erase(edge);

            // LLL

            for(list<Node>::iterator it = adjl[i].begin(); it != adjl[i].end();){
                int cluster_center = cluster[it->v];

                auto v = smallest_edge[cluster_center];

                if (mark_center[cluster_center]) {
                    if (!seen[cluster_center]) {
                        spanner_edges.push_back({i, v.fr, v.sc});
                        seen[cluster_center] = 1;
                    }
                    
                    adjl[it->v].erase(it->sibling);
                    it = adjl[i].erase(it);
                }
                else
                    it++;
            }

            
        }
        // End of Step 3

        // Start of Step 4: Removing intra-cluster edges

        for (int i = 1; i <= n; i++) {
            if (is_cluster[i]) continue;

            vector<pii> intra_cluster_edges = {};
            int cluster_center = cluster[i];
            if (!is_cluster[cluster_center]) continue;

            // for (auto u : adj[i]) {
            //     if (u.fr == cluster_center) {
            //         cout << "u.fr cannot be equal to cluster_center, check program\n";
            //         continue;
            //     }

            //     if (cluster[u.fr] == cluster_center) {
            //         // this is an intra cluster edge
            //         adj[u.fr].erase({i, u.sc});
            //         intra_cluster_edges.push_back(u);
            //     }
            // }
            
            // // delete the intra cluster edge from the graph
            // for (auto edge : intra_cluster_edges) adj[i].erase(edge);

            // LLL

            for (list<Node>::iterator it = adjl[i].begin(); it != adjl[i].end();) {
                if (it->v == cluster_center) {
                    cout << "u.fr cannot be equal to cluster_center, check program\n";
                    continue;
                }

                if (cluster[it->v] == cluster_center) {
                    // this is an intra cluster edge
                    adjl[it->v].erase(it->sibling);
                    it = adjl[i].erase(it);
                }
                else
                    it++;
            }

        }
    }
    
    // End of Phase 1
    auto phase1_end = high_resolution_clock::now();
    phase_one_edge_count = spanner_edges.size();
    
    // Start of Phase 2: Vertex-Cluster joining

    // just a safety check that we had (k - 1) iterations
    assert(iter == k);

    int idx = (iter + 1) % 2;
    phase2_cluster_count = cluster_centers[idx].size();

    auto phase2_start = high_resolution_clock::now();
    for (int i = 1; i <= n; i++) {
        // smallest edge from i to all the final clusters (C_{k - 1})
        // vector<pii> smallest_edge(n + 10, {0, INF});

        // vector<pii> delete_edges = {}; // edges to be deleted from original graph

        // // finding smallest edges from node i to all the clusters
        // for (auto u : adj[i]) {
        //     int cluster_center = cluster[u.fr];

        //     auto v = smallest_edge[cluster_center];

        //     if (u.sc < v.sc) {
        //         delete_edges.push_back(v);
        //         adj[v.fr].erase({i, v.sc});
        //         smallest_edge[cluster_center] = u;
        //     }
        //     else {
        //         delete_edges.push_back(u);
        //         adj[u.fr].erase({i, u.sc});
        //     }
        // }

        // // delete the non-smallest edges from node i to some node in other cluster
        // for (auto edge : delete_edges) adj[i].erase(edge);

        // // adding all the smallest edges to the spanner graph
        // for (auto u : adj[i]) {
        //     spanner_edges.push_back({i, u.fr, u.sc});
        //     adj[u.fr].erase({i, u.sc});
        // }

        // adj[i].clear(); // removing all the edges added to spanner graph
    
        // LLL

        vector<list<Node>::iterator> smallest_edge_iterators(n + 10, adjl[i].end());

        //  Remove nodes larger than the smallest
        for(list<Node>::iterator it = adjl[i].begin(); it != adjl[i].end();){
            int cluster_center = cluster[it->v];

            auto sm = smallest_edge_iterators[cluster_center];

            if (sm == adjl[i].end() || it->w < sm->w) {
                // delete_edges.push_back(v);
                if(sm != adjl[i].end()){
                    adjl[sm->v].erase(sm->sibling);
                    adjl[i].erase(sm);
                }

                smallest_edge_iterators[cluster_center] = it;
                it++;
            }
            else {
                // delete_edges.push_back({it->v, it->w});
                adjl[it->v].erase(it->sibling);
                it = adjl[i].erase(it);
            }
        }

        // add smallest to spanner and remove from adjl
        for(list<Node>::iterator it = adjl[i].begin(); it != adjl[i].end();){
            spanner_edges.push_back({i, it->v, it->w});
            adjl[it->v].erase(it->sibling);
            it = adjl[i].erase(it);
        }

    }

    // End of Phase 2
    auto phase2_end = high_resolution_clock::now();

    int total_edges = spanner_edges.size();
    phase_two_edge_count = total_edges - phase_one_edge_count;
    
    // Printing the Final spanner graph

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
}
