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

void distances(vector<vector<pair<int, int>>>& adj, vector<vector<int>>& dists){
    int n = adj.size();
    for(int i = 0; i < n; i++){
        vector<int> p;
        dijkstra(i, dists[i], p, adj);
    }
}


int main(){
    int t;
    cin>>t;
    int n, m;
    cin>>n>>m;
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
    vector<vector<int>> dists(n, vector<int>());
    vector<vector<int>> dists2(n2, vector<int>());
    distances(adj, dists);
    distances(adj2, dists2);
    bool ok = true;
    for(int i = 0; i < n; i++){
        for(int j = 0; j < n; j++){
            if(dists2[i][j] > t * dists[i][j]){
		cout<<i<<" "<<j<<" "<<dists[i][j]<<" "<<dists2[i][j]<<endl;
                ok = false;
                break;
            }
        }
    }
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
    if(ok)
        cout<<"YES"<<endl;
    else
        cout<<"NO"<<endl;
    return 0;
}
