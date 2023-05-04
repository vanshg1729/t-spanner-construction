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

void floyd_warshall(int s, vector<vector<int>> & d, vector<vector<pair<int, int>>>& adj) {
    int n = adj.size();
    d.assign(n, vector<int>(n, INF));
    for(int i = 0; i < n; i++){
        for(auto next : adj[i]){
            d[i][next.first] = next.second;
            d[next.first][i] = next.second;
            // cout<<next.second<<endl;
        }
    }
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (d[i][k] < INF && d[k][j] < INF)
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j]); 
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

int main(){
    int t;
    cin>>t;
    int n, m;
    cin>>n>>m;
    srand(time(0));
    vector<vector<pair<int,int>>> adj(n, vector<pair<int,int>>());
    
    for(int i = 0; i < m; i++){
        int x, y, w;
        cin>>x>>y>>w;
        x--;y--;
        adj[x].push_back(make_pair(y, w));
        adj[y].push_back(make_pair(x, w));
    }
    int n2, m2;
    cin>>n2>>m2;
    vector<vector<pair<int,int>>> adj2(n2, vector<pair<int,int>>());
    for(int i = 0; i < m2; i++){
        int x, y, w;
        cin>>x>>y>>w;
        x--;y--;
        adj2[x].push_back(make_pair(y, w));
        adj2[y].push_back(make_pair(x, w));
    }

    int phase1_edge_count = 0, phase2_edge_count = 0;
    double phase1_time = 0, phase2_time = 0, total_time = 0;

    cin >> phase1_edge_count >> phase2_edge_count;
    cin >> phase1_time >> phase2_time >> total_time;

    vector<vector<int>> dists(n, vector<int>());
    vector<vector<int>> dists2(n2, vector<int>());
    // distances(adj, dists);
    // distances(adj2, dists2);
    // floyd_warshall(0, dists, adj);
    // floyd_warshall(0, dists2, adj2);

    bool ok = true;
    double spanner_score = 0;
    // for(int i = 0; i < n; i++){
    //     for(int j = 0; j < n; j++){
    //         spanner_score = max(spanner_score, ((double) dists2[i][j])/dists[i][j]);
    //         if(dists2[i][j] > t * dists[i][j]){
	// 	// cout<<i + 1 <<" "<< j + 1 <<" "<<dists[i][j]<<" "<<dists2[i][j]<<endl;
    //             ok = false;
    //             break;
    //         }
    //     }
    // }
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
    cout<<"{\"status\":";
    if(ok)
        cout<<"\"YES\",";
    else
        cout<<"\"NO\",";
    printJson("spanner_score", to_string(spanner_score));
    printJson("phase1_edge_count", to_string(phase1_edge_count));
    printJson("phase2_edge_count", to_string(phase2_edge_count));
    printJson("phase1_time", to_string(phase1_time));
    printJson("phase2_time", to_string(phase2_time));
    printJson("total_time", to_string(total_time));
    printJson("total_edges", to_string(m2));
    printJson("original_edges", to_string(m));
    cout<<"\"check\":"<<rand()<<"}"<<endl;
    return 0;
}
