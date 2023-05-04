## Folder structure

- Implementations/
- Generators/
- Testcases/
	- Dataset/
		- Sparse/
			Sparse_test_x.txt
		- Dense/
	- Temp/
- Output/
	- Test_instance_x/
		- metadata.json
		- implementation.cpp
		- generator.cpp
- DebugLab/
- bin/

## Test suite
- Multitest for same n and t (done)
- Multitest for same n but different t (to plot number of spanner-edges vs
t) - one for cluster-cluster, one for original
- Multitest with same t but different n (to plot time complexity of
t-spanner)
