# t-spanner-construction
Implementing and analysing the t-spanner construction algorithm by Baswana and Sen

## Clone
To clone the repository, run the command:

```
git clone https://github.com/fine-man/t-spanner-construction.git
```
- [Link to the repository](https://github.com/fine-man/t-spanner-construction)

## Setup

We need a few python packages to run the test-suite. Run the following:
```
pip3 install -r test-suite/requirements.txt
```

## Using the test-suite

To see the list of commands available
```
python3 test-suite/main.py --help
```

### Commands
``` 
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ create-dataset        Create a Dataset with a single n value                                                                                        │
│ create-ndata          Create a Dataset with different n values                                                                                      │
│ ntest                 Test a particular implementation on a single t_value with different n values                                                  │
│ test-data             Test an implementation on a dataset with a particular t-value                                                                 │
│ ttest                 Test a particular implementation with a particular number of nodes and different t values                                     │
│ ttest-data            Test an implementation on a dataset with different t-values                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

To see the help for a particular command, use `--help` with the name of the
command like this:
```
python3 test-suite/main.py <command-name> --help
```

## Generating the Datasets
We generate two kinds of datasets, one with varying `n-values` which can be
later used by `test-data` command and another kind of dataset is with same
`n-value` which can be used by the `ttest-data` command.

### create-dataset
This command can be used to generate multiple dense graphs with the same
`n-value`. 

#### Arguments
This command takes the following arguments:

```
 Usage: main.py create-dataset [OPTIONS] GENERATOR NO_OF_NODES NO_OF_TESTS

 Create a Dataset with a single n value

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    generator        TEXT     [default: None] [required]                                                                                           │
│ *    no_of_nodes      INTEGER  [default: None] [required]                                                                                           │
│ *    no_of_tests      INTEGER  [default: None] [required]                                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
`generator` is the path to the particular graph generator used,
`no_of_nodes` is the `n_value` and `no_of_tests` tells the number of graphs
to generate. 

#### Example
A test run would look something like this:

```
$ python3 test-suite/main.py create-dataset dgg.cpp 200 5
```
Output :
```
Generating tests in ./datasets/dataset-582381/
Generating test: #1/5 at ./datasets/dataset-582381/test-0.txt
Generating test: #2/5 at ./datasets/dataset-582381/test-1.txt
Generating test: #3/5 at ./datasets/dataset-582381/test-2.txt
Generating test: #4/5 at ./datasets/dataset-582381/test-3.txt
Generating test: #5/5 at ./datasets/dataset-582381/test-4.txt
Written all testcases to ./datasets/dataset-582381/
```
The generated dataset is stored in the `datasets` directory

### create-ndata
This command generate dense graphs with different `n-values`. The resulting
dataset can be used by `test-data` to test the implementation with a
particular `t-value`. 

#### Arguments
The command takes the following arguments:

```
 Usage: main.py create-ndata [OPTIONS] GENERATOR NO_OF_TESTS

 Create a Dataset with different n values

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    generator        TEXT     [default: None] [required]                                                                                           │
│ *    no_of_tests      INTEGER  [default: None] [required]                                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --nstart             TEXT  [default: 3]                                                                                                             │
│ --nend               TEXT  [default: 100]                                                                                                           │
│ --ninc               TEXT  [default: 10]                                                                                                            │
│ --custom-data        TEXT  [default: []]                                                                                                            │
│ --help                     Show this message and exit.                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
The optional arguments tells the range of `n-values`. `no_of_tests` number
of graphs will be generated for all n values in `range(nstart, nend + 1, ninc)`

#### Example
A test run of this command would look something like this:
```
$ python3 test-suite/main.py create-ndata dgg.cpp 2 --nstart 100 --nend 101 --ninc 1
```
Output:
```
Generating tests in ./datasets/dataset-583456/
Generating test: #1/4 with n_value = 100 at ./datasets/dataset-583456/test-100-0.txt
Generating test: #2/4 with n_value = 100 at ./datasets/dataset-583456/test-100-1.txt
Generating test: #3/4 with n_value = 101 at ./datasets/dataset-583456/test-101-0.txt
Generating test: #4/4 with n_value = 101 at ./datasets/dataset-583456/test-101-1.txt
Written all testcases to ./datasets/dataset-583456/
```
The generated dataset is stored in the `datasets` directory

## Running the different implementations on Datasets
After generating datasets, we can start running the different
implementations on these datasets. We have two commands that can be used to
test the different implementations on the datasets

### test-data
This command tests an implementation on a dataset with a particular
`t-value`.

#### Arguments
This command takes the following arguments

```
 Usage: main.py test-data [OPTIONS] IMPL DATASET_PATH T_VALUE

 Test an implementation on a dataset with a particular t-value

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    impl              TEXT     [default: None] [required]                                                                                          │
│ *    dataset_path      TEXT     [default: None] [required]                                                                                          │
│ *    t_value           INTEGER  [default: None] [required]                                                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --checker-args        TEXT                                                                                                                          │
│ --help                      Show this message and exit.                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
`impl` is the path to the particular implementation. The optional argument
`--checker-args` tells the test-suite whether to check for correctness of
the implementation as well, by default the option is set to off. Use
`--checker-args 1` to set this option.

#### Example
A test run of this command would look something like this:
```
$ python3 test-suite/main.py test-data ./implementations/t-spanner.cpp ./datasets/dataset-583456/ 3 --checker-args 1 
```
The results of the tests will be stored in a folder inside the `outputs`
directory.

### ttest-data
The command tests an implementation on a dataset with different t-values

#### Arguments
This command takes the following arguments:
```
 Usage: main.py ttest-data [OPTIONS] IMPL DATASET_PATH NO_OF_NODES

 Test an implementation on a dataset with different t-values

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    impl              TEXT     [default: None] [required]                                                                                          │
│ *    dataset_path      TEXT     [default: None] [required]                                                                                          │
│ *    no_of_nodes       INTEGER  [default: None] [required]                                                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --tstart              TEXT  [default: 3]                                                                                                            │
│ --tend                TEXT  [default: 100]                                                                                                          │
│ --tinc                TEXT  [default: 10]                                                                                                           │
│ --checker-args        TEXT                                                                                                                          │
│ --help                      Show this message and exit.                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
The optional arguments `tstart`, `tend` and `tinc` tells the test-suite
what `t-values` to test on. The test-suite will test using all values in
the `range(tstart, tend, tinc)`. 

#### Example
A test run of this command would look something like this:
```
$ python3 test-suite/main.py ttest-data ./implementations/t-spanner.cpp ./datasets/dataset-583440/ 100 --tstart 25 --tend 100 --tinc 25
```
The results of the tests will be stored in a folder inside the `outputs` directory.

## Plotting the values for the test runs
After generating the outputs of the test runs, we can finally start
plotting the values of the result against different `n-values` and different
`t-values`

### tvalue-graphs
To generate plots of any attribute against `t-value`, `cd` to the directory
`./plot-graphs/tvalue-graphs/` and then copy the output directory into the
current directory like this : `cp -r ../../outputs/<output_dir> .` <br>
After copying the output directories, use the python scripts to generate
the plots

#### scripts
These are all the scripts present in `tvalue-graphs` directory:
```
tvalue-vs-complexity.py
tvalue-vs-edges.py
tvalue-vs-phase-time.py
tvalue-vs-phase-edge.py
tvalue-vs-cluster-count.py
```
The syntax to run a particular script is:
```
python3 <script-name> [<output_dir>/info.json ...]
```

#### Example
A test command would look something like this:
```
$ python tvalue-vs-complexity.py output-427303/info.json output-427409/info.json
```
Single or multiple output folders can be used to generate plots using
results of single or multiple tests.

### nvalue-graphs
To generate plots of any attribute against `t-value`, `cd` to the directory
`./plot-graphs/nvalue-graphs/` and then copy the output directory into the
current directory like this : `cp -r ../../outputs/<output_dir> .` <br>
After copying the output directories, use the python scripts to generate
the plots

#### scripts
These are all the scripts present in `nvalue-graphs` directory:
```
nvalue-vs-complexity.py
nvalue-vs-edges.py
nvalue-vs-phase-time.py
nvalue-vs-phase-edge.py
nvalue-vs-cluster-count.py
```
The syntax to run a particular script is:
```
python3 <script-name> [<output_dir>/info.json ...]
```

#### Example
A test command would look something like this:
```
$ python nvalue-vs-complexity.py output-427303/info.json output-427409/info.json
```
Single or multiple output folders can be used to generate plots using
results of single or multiple tests.
