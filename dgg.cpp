#include <bits/stdc++.h>

using namespace std;
int main(int argc, char** argv){
	int n = atoi(argv[1]); // dum dum
	srand(time(0));
	std::default_random_engine generator;
	std::normal_distribution<double> distribution(100.0, 100.0);
	vector<vector<pair<int,int>>> adj(n, vector<pair<int,int>>());
	int edges= 0;
	for(int i = 0; i < n; i++){
		for(int j = 0; j < n; j++){
			if(i <= j)
				continue;
			int rand_num = distribution(generator);
			int w = max(0, rand_num);
			if(w != 0){
				adj[i].push_back({j, w});
				adj[j].push_back({i, w});
				edges++;
			}	
		}
	}

	cout<<n<<" "<<edges<<endl;
	for(int i = 0; i < n; i++){
		for(auto p : adj[i]){
			if(p.first <= i)
				continue;
			cout<<i+1<<" "<<p.first+1<<" "<<p.second<<endl;
		}
	}
	return 0;
}
