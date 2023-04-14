// #include <iostream>
// #include <fstream>
// #include <utility>
// #include <cstdlib>
// #include <time.h>
// #include <vector>
// #include <assert.h>
#include <bits/stdc++.h>

using namespace std;

bool choose(int n){
	int threshold = sqrt(n);
	if(rand()%n <= threshold){
		return true;
	}
	return false;
}

void choose_cluster_centers(int n, vector<int>& sampled_nodes){
	for(int i = 0; i < n; i++){
		if(choose(n))
			sampled_nodes.push_back(i);
	}
}

int main(){
	srand(time(0));
	/* Open input file */
	ifstream input_file;
	input_file.open("in.txt");
	assert(input_file.is_open());
	
	/* Get the graph */
	int n, m; // n = no of nodes, m = no of edges
	input_file >> n >> m;

	/* 
		IDEA: Maybe we should use regular adj list and 
		use a map to keep track of weights of edges
	*/

	vector<vector<pair<int,int>>> adjacency_list(n, vector<pair<int,int>>());
	// First number in pair is the adjacent node and second is the weight of edge

	for(int j = 0; j < m; j++){
		int x, y, w;
		input_file >> x >> y >> w;
		adjacency_list[x].push_back(make_pair(y, w));
		adjacency_list[y].push_back(make_pair(x, w));
	}

	vector<vector<pair<int,int>>> new_adjacency_list(n, vector<pair<int,int>>());

	vector<int> sampled_nodes;
	choose_cluster_centers(n, sampled_nodes);
	/* NOTE: sampled_nodes will be in sorted order of index */	

	/* Find adjacent nodes to the cluster points*/
	set<int> adjacent_nodes;
	for(auto node : sampled_nodes){
		for(auto e : adjacency_list[node]){
			adjacent_nodes.insert(e.first);
		}
	}

	for()
	

	/* close input file*/
	input_file.close();
}
