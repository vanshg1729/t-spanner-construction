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
    vector<vector<pair<int,int>>> adj2(n2, vector<pair<int,int>>());
    for(int i = 0; i < m2; i++){
        int x, y, w;
        cin >> x >> y >> w;
        x--; y--;
        adj2[x].push_back({y, w});
        adj2[y].push_back({x, w});
    }

    // t-spanner stat variables
    int phase1_edge_count = 0, phase2_edge_count = 0;
    double phase1_time = 0, phase2_time = 0, total_time = 0;
    bool ok = true;
    double spanner_score = 0;

    // graph stat variables
    double avg_path_len = 0;
    int min_path_len = INF, max_path_len = 0;
    int paths_atleast_t = 0; // number of paths whose length >= k

    cin >> phase1_edge_count >> phase2_edge_count;
    cin >> phase1_time >> phase2_time >> total_time;

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

        for(int i = 0; i < n; i++){
            for(int j = 0; j < n; j++){
                if (i == j) continue;
                spanner_score = max(spanner_score, ((double) dists2[i][j])/dists[i][j]);
                min_path_len = min(min_path_len, path_lengths[i][j]);
                max_path_len = max(max_path_len, path_lengths[i][j]);
                avg_path_len += path_lengths[i][j];

                if (path_lengths[i][j] >= t) paths_atleast_t++;
                if(dists2[i][j] > t * dists[i][j]){
        	// cout<<i + 1 <<" "<< j + 1 <<" "<<dists[i][j]<<" "<<dists2[i][j]<<endl;
                    ok = false;
                    break;
                }
            }
        }

        avg_path_len /= n * (n - 1);

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
    printJson("min_path_len", to_string(min_path_len));
    printJson("avg_path_len", to_string(avg_path_len));
    printJson("max_path_len", to_string(max_path_len));
    printJson("paths_atleast_t", to_string(paths_atleast_t));
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
    cout<<"\"check\":"<<rand()<<"}"<<endl;
    return 0;
}
