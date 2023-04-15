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

void choose_cluster_centers(int n, vector<bool>& is_sampled, vector<int>& sampled_nodes){
	for(int i = 0; i < n; i++){
		if(choose(n)){
			sampled_nodes.push_back(i);
			is_sampled[i] = true;
		}
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
	vector<bool> is_sampled(n, false);
	choose_cluster_centers(n, is_sampled, sampled_nodes);
	/* NOTE: sampled_nodes will be in sorted order of index */	

	/* Find adjacent nodes to the cluster points*/
	set<int> adjacent_nodes;
	vector<bool> is_adjacent_node(n, false);
	for(auto node : sampled_nodes){
		for(auto e : adjacency_list[node]){

			// Don't insert sampled nodes
			if(binary_search(sampled_nodes.begin(), sampled_nodes.end(), e.first))
				continue;
			
			adjacent_nodes.insert(e.first);
			is_adjacent_node[e.first] = true;
		}
	}

	// PHASE 1: Forming the clusters

	/* Add all edges for non adjacent nodes */
	for(int i = 0; i < n; i++){
		if(binary_search(sampled_nodes.begin(), sampled_nodes.end(), i))
			continue;
		if(adjacent_nodes.find(i) != adjacent_nodes.end())
			continue;
		for(auto e : adjacency_list[i]){
			new_adjacency_list[i].push_back(e);
			new_adjacency_list[e.first].push_back(make_pair(i, e.second));
		}
	}

	vector<int> parent(n, 0);
	for(auto node : sampled_nodes){
		parent[node] = node;
	}
	// VERY INEFFICIENT CODE COMING UP
	for(auto i : adjacent_nodes){
		
		// get the edge that is the smallest to a sampled node
		int min_weight_to_sampled = INT_MAX; // NOTE: Change accordingly
		for(auto e : adjacency_list[i]){
			if(is_sampled[e.first])
				min_weight_to_sampled = min(min_weight_to_sampled, e.second);
		}

		// insert the min edge to a sampled node to the new graph
		for(auto e : adjacency_list[i]){
			if(is_sampled[e.first] && e.second == min_weight_to_sampled){
				new_adjacency_list[i].push_back(e);
				new_adjacency_list[e.first].push_back(make_pair(i, e.second));
				parent[i] = e.first;
				break;
			}
		}

		// insert all edges which have smaller weight
		for(auto e : adjacency_list[i]){
			// if(!is_sampled[e.first] && !is_adjacent_node[e.first]){ // NOTE: try removing the adjacent condition
				if(e.second < min_weight_to_sampled){
					new_adjacency_list[i].push_back(e);
					new_adjacency_list[e.first].push_back(make_pair(i, e.second));
				}
			// }
		}
	}

	// TODO: Remove intercluster edges
	
	// Phase 2 : Joining vertices with their neighbouring clusters

	for(int i = 0; i < n; i++){
		if(!is_sampled[i] && !is_adjacent_node[i])
			continue;
		map<int,int> neighbour;
		map<int,int> weight;
		int mx = INT_MAX;
		for(auto e : adjacency_list[i]){

			// because non adjacent nodes are not part of any cluster
			if(!is_sampled[e.first] && !is_adjacent_node[e.first])
				continue;
			
			if(weight[parent[e.first]] < mx - e.second){
				neighbour[parent[e.first]] = e.first;
				weight[parent[e.first]] = mx - e.second;
			}
		}

		for(auto p : weight){
			int x = i;
			int y = neighbour[p.first];
			int w = mx - p.second;
			new_adjacency_list[x].push_back(make_pair(y, w));
			new_adjacency_list[y].push_back(make_pair(x, w));
		}
	}


	/* close input file*/
	input_file.close();
}

