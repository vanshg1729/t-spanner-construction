#include <bits/stdc++.h>

using namespace std;

const int INF = 1000000000;

void dijkstra(int s, vector<int> & d, vector<int> & p, vector<vector<pair<int, int>>>& adj) {
    int n = adj.size();
    d.assign(n, INF);
    p.assign(n, -1);
    vector<bool> u(n, false);

    d[s] = 0;
    for (int i = 0; i < n; i++) {
        int v = -1;
        for (int j = 0; j < n; j++) {
            if (!u[j] && (v == -1 || d[j] < d[v]))
                v = j;
        }

        if (d[v] == INF)
            break;

        u[v] = true;
        for (auto edge : adj[v]) {
            int to = edge.first;
            int len = edge.second;

            if (d[v] + len < d[to]) {
                d[to] = d[v] + len;
                p[to] = v;
            }
        }
    }
}

void floyd_warshall(int s, vector<vector<int>> & d, vector<vector<pair<int, int>>>& adj,
        vector<vector<int>> & path_lengths) {
    int n = adj.size();
    d.assign(n, vector<int>(n, INF));
    path_lengths.assign(n, vector<int>(n, 0));

    for(int i = 0; i < n; i++){
        for(auto next : adj[i]){
            d[i][next.first] = next.second;
            d[next.first][i] = next.second;
            path_lengths[i][next.first] = 1;
            path_lengths[next.first][i] = 1;
            // cout<<next.second<<endl;
        }
    }

    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (d[i][k] < INF && d[k][j] < INF && d[i][k] + d[k][j] < d[i][j]) {
                    d[i][j] = d[i][k] + d[k][j];
                    path_lengths[i][j] = path_lengths[i][k] + path_lengths[k][j];
                }
            }
        }
    }

    // for(int i = 0; i < n; i++){
    //     for(int j = 0; j < n; j++){
    //         cout<<d[i][j]<<" ";
    //     }
    //     cout<<endl;
    // }

}


void distances(vector<vector<pair<int, int>>>& adj, vector<vector<int>>& dists){
    int n = adj.size();
    for(int i = 0; i < n; i++){
        vector<int> p;
        dijkstra(i, dists[i], p, adj);
    }
}

void printJson(string a, string b){
    cout<<"\""<<a<<"\":"<<"\""<<b<<"\",";
}

int main(int argc, char *argv[]){
    bool calculate_distances = false;

    if (argc > 1) {
        if (atoi(argv[1]) == 1) calculate_distances = true;
    }

    srand(time(0));
    int t;
    cin >> t;

    // taking input of the first graph
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int,int>>> adj(n, vector<pair<int,int>>());
    
    for(int i = 0; i < m; i++){
        int x, y, w;
        cin >> x >> y >> w;
        x--; y--;
        adj[x].push_back({y, w});
        adj[y].push_back({x, w});
    }

    // taking input of t-spanner graph of the first graph
    int n2, m2;
    cin >> n2 >> m2;
    assert(n == n2);
    vector<vector<pair<int,int>>> adj2(n2, vector<pair<int,int>>());
    for(int i = 0; i < m2; i++){
        int x, y, w;
        cin >> x >> y >> w;
        x--; y--;
        adj2[x].push_back({y, w});
        adj2[y].push_back({x, w});
    }

    // calculating t-spanner stat variables
    int phase1_edge_count = 0, phase2_edge_count = 0, phase2_cluster_count = 0;
    double phase1_time = 0, phase2_time = 0, total_time = 0;
    bool ok = true;
    double spanner_score = 0;

    // graph stat maps
    map<string, double> original_stat, spanner_stat;
    original_stat["connected"] = 1, spanner_stat["connected"] = 1;
    original_stat["avg_path_len"] = 0, spanner_stat["avg_path_len"] = 0;
    original_stat["min_path_len"] = INF, spanner_stat["min_path_len"] = INF;
    original_stat["max_path_len"] = 0, spanner_stat["max_path_len"] = 0;
    original_stat["paths_atleast_t"] = 0, spanner_stat["paths_atleast_t"] = 0;

    cin >> phase1_edge_count >> phase2_edge_count;
    cin >> phase1_time >> phase2_time >> total_time;
    cin >> phase2_cluster_count;

    // calculating distances and all the stat variables
    if (calculate_distances) {
        vector<vector<int>> dists(n, vector<int>());
        vector<vector<int>> dists2(n2, vector<int>());
        vector<vector<int>> path_lengths(n, vector<int>());
        vector<vector<int>> path_lengths2(n2, vector<int>());

        //distances(adj, dists);
        //distances(adj2, dists2);
        floyd_warshall(0, dists, adj, path_lengths);
        floyd_warshall(0, dists2, adj2, path_lengths2);

        // iterating over distances of original graph
        for(int i = 0; i < n; i++){
            for(int j = 0; j < n; j++){
                if (i == j) continue;
                spanner_score = max(spanner_score, ((double) dists2[i][j])/dists[i][j]);
                original_stat["min_path_len"] = min(original_stat["min_path_len"], (double) path_lengths[i][j]);
                original_stat["max_path_len"] = max(original_stat["max_path_len"], (double) path_lengths[i][j]);
                original_stat["avg_path_len"] += (double) path_lengths[i][j];
                if (path_lengths[i][j] >= t) original_stat["paths_atleast_t"]++;
                if (dists[i][j] == INF) original_stat["connected"] = 0;

                spanner_stat["min_path_len"] = min(spanner_stat["min_path_len"], (double) path_lengths2[i][j]);
                spanner_stat["max_path_len"] = max(spanner_stat["max_path_len"], (double) path_lengths2[i][j]);
                spanner_stat["avg_path_len"] += (double) path_lengths2[i][j];
                if (path_lengths2[i][j] >= t) spanner_stat["paths_atleast_t"]++;
                if (dists2[i][j] == INF) spanner_stat["connected"] = 0;

                if(dists2[i][j] > t * dists[i][j]){
        	// cout<<i + 1 <<" "<< j + 1 <<" "<<dists[i][j]<<" "<<dists2[i][j]<<endl;
                    ok = false;
                    break;
                }
            }
        }

        original_stat["avg_path_len"] /= (double) n * (n - 1);
        spanner_stat["avg_path_len"] /= (double) n * (n - 1);

    /*    for(auto v : dists){
            for(auto x : v){
                cout<<x<<" ";
            }
            cout<<endl;
        }

        for(auto v : dists2){
            for(auto x : v){
                cout<<x<<" ";
            }
            cout<<endl;
        }*/
    }

    // print all the stat information
    cout<<"{\"status\":";
    if(calculate_distances) {
        if (ok) {
            cout << "\"YES\",";
        }
        else {
            cout << "\"NO\",";
        }
    }
    else {
        cout << "\"NA\",";
    }
    printJson("calculate_distances", to_string(calculate_distances));

    for (auto item : original_stat) {
        auto key = item.first;
        auto value = item.second;
        if (calculate_distances) {
            printJson("original_" + key, to_string(value));
        }
        else {
            printJson("original_" + key, "NA");
        }
    }

    for (auto item : spanner_stat) {
        auto key = item.first;
        auto value = item.second;
        if (calculate_distances) {
            printJson("spanner_" + key, to_string(value));
        }
        else {
            printJson("spanner_" + key, "NA");
        }
    }

    printJson("n_value", to_string(n));
    printJson("t_value", to_string(t));
    printJson("spanner_score", to_string(spanner_score));
    printJson("phase1_edge_count", to_string(phase1_edge_count));
    printJson("phase2_edge_count", to_string(phase2_edge_count));
    printJson("phase1_time", to_string(phase1_time));
    printJson("phase2_time", to_string(phase2_time));
    printJson("total_time", to_string(total_time));
    printJson("total_edges", to_string(m2));
    printJson("original_edges", to_string(m));
    printJson("no_of_nodes", to_string(n));
    printJson("phase2_cluster_count", to_string(phase2_cluster_count));
    cout<<"\"check\":"<<rand()<<"}"<<endl;
    return 0;
}
