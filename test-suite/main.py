import typer
import os
import json
# import timer
import tqdm
import subprocess
import time
import math

app = typer.Typer()

start_time = 1683228252

@app.command()
def create_dataset(generator: str, no_of_nodes: int, no_of_tests: int):
    """
    Create a Dataset with a single n value
    """
    dataset_num = math.floor(time.time()) - start_time
    dir_name = "./datasets/dataset-" + str(dataset_num) + "/"
    os.system(f"mkdir {dir_name}")
    generator_basename = os.path.basename(generator)

    gen_src = dir_name + generator_basename
    gen_bin = dir_name + "generator.out"
    os.system("cp " + generator + " " + gen_src)
    os.system("g++ " + gen_src + " -o " + gen_bin)

    print(f"Generating tests in {dir_name}")
    for idx in range(no_of_tests):
        test_case = dir_name + "test-" + str(idx) + ".txt"
        print(f"Generating test: #{idx + 1}/{no_of_tests} at {test_case}", flush=True)
        os.system(gen_bin + " " + str(no_of_nodes) + " > " + test_case)

    print(f"Written all testcases to {dir_name}")


@app.command()
def create_ndata(generator: str, no_of_tests: int, nstart=3, nend=100, ninc=10):
    """
    Create a Dataset with different n values
    """
    nstart = max(3, int(nstart))
    nend = int(nend)
    ninc = int(ninc)
    n_values = [ i for i  in range(nstart, nend+1, ninc)]

    dataset_num = math.floor(time.time()) - start_time
    dir_name = "./datasets/dataset-" + str(dataset_num) + "/"
    os.system(f"mkdir {dir_name}")
    generator_basename = os.path.basename(generator)

    gen_src = dir_name + generator_basename
    gen_bin = dir_name + "generator.out"
    os.system("cp " + generator + " " + gen_src)
    os.system("g++ " + gen_src + " -o " + gen_bin)

    total_tests = len(n_values) * no_of_tests
    print(f"Generating tests in {dir_name}")
    for i, n_value in enumerate(n_values):
        for idx in range(no_of_tests):
            test_num = i * no_of_tests + idx + 1
            testcase_path = dir_name + "test-" + str(n_value) + "-" + str(idx) + ".txt"
            print(f"Generating test: #{test_num}/{total_tests} with n_value = {n_value} at {testcase_path}", flush=True)
            os.system(gen_bin + " " + str(n_value) + " > " + testcase_path)

    print(f"Written all testcases to {dir_name}")

@app.command()
def doTest(impl: str, generator: str, no_of_nodes: int, t_value: int):
    with open("./outputs/metadata.json", "r") as f:
        metadata = json.load(f)
    test_number = math.floor(time.time()) - start_time
    info = {}
    info['cmd'] = 'dotest'
    info['n_value'] = no_of_nodes
    info['t_value'] = t_value
    dir_name = "./outputs/output-" + str(metadata['outputs']) + "/"
    os.system("mkdir " + dir_name)

    impl_basename = os.path.basename(impl)
    generator_basename = os.path.basename(generator)

    info_json = dir_name + "info.json"
    impl_src = dir_name + impl_basename
    gen_src = dir_name + generator_basename
    impl_bin = dir_name + "impl.out"
    gen_bin = dir_name + "generator.out"
    test_case = dir_name + "test-" + str(test_number) + ".txt"
    test_output = dir_name + "out-" + str(test_number) + ".txt"
    checker_input = dir_name + "checker-input-" + str(test_number) + ".txt"

    with tqdm.tqdm(total=70) as pbar:
        os.system("cp " + impl + " " + impl_src)
        pbar.update(10)
        os.system("cp " + generator + " " + gen_src)
        pbar.update(10)
        os.system("g++ " + impl_src + " -o " + impl_bin)
        pbar.update(10)
        os.system("g++ " + gen_src + " -o " + gen_bin)
        pbar.update(10)
        os.system(gen_bin + " " + str(no_of_nodes) + " > " + test_case)
        pbar.update(10)
        os.system(impl_bin + " " + str(t_value) + " < " + test_case + " > " + test_output)
        pbar.update(10)
        os.system("echo " + str(t_value) + " > " + checker_input)
        os.system("cat " + test_case + " >> " + checker_input)
        os.system("cat " + test_output + " >> " + checker_input)
        os.system("g++ checker.cpp -o check")
        os.system("./check < " + checker_input)
        check_output = subprocess.run("./check < " + checker_input, shell=True, capture_output=True, text=True)
        pbar.update(10)
        # print(check_output.stdout)
        check_output_json = (json.loads(check_output.stdout))
    info['status'] = check_output_json['status']
    info['spanner_score'] = check_output_json['spanner_score']
    metadata['outputs'] += 1
    with open('./outputs/metadata.json', 'w') as f:
        json.dump(metadata, f)  
    with open(info_json, 'w') as f:
        json.dump(info, f, indent=4)
    
    print(json.dumps(info, indent=4))

@app.command()
def multiTest(impl: str, generator: str, no_of_nodes: int, t_value: int, no_of_tests: int):
    with open("./outputs/metadata.json", "r") as f:
        metadata = json.load(f)
    test_number = math.floor(time.time()) - start_time
    info = {}
    info['cmd'] = 'mutitest'
    info['n_value'] = no_of_nodes
    info['t_value'] = t_value
    info['no_of_tests'] = no_of_tests
    dir_name = "./outputs/output-" + str(metadata['outputs']) + "/"
    os.system("mkdir " + dir_name)

    impl_basename = os.path.basename(impl)
    generator_basename = os.path.basename(generator)

    info_json = dir_name + "info.json"
    impl_src = dir_name + impl_basename
    gen_src = dir_name + generator_basename
    impl_bin = dir_name + "impl.out"
    gen_bin = dir_name + "generator.out"

    os.system("cp " + impl + " " + impl_src)
    os.system("cp " + generator + " " + gen_src)
    os.system("g++ " + impl_src + " -o " + impl_bin)
    os.system("g++ " + gen_src + " -o " + gen_bin)
    os.system("g++ checker.cpp -o check")

    print("Generating tests ... ")
    for idx in range(no_of_tests):
        print("Generating test: #", idx, flush=True)
        test_case = dir_name + "test-" + str(test_number) + '-' + str(idx) + ".txt"
        test_output = dir_name + "out-" + str(test_number) + '-' + str(idx) + ".txt"
        checker_input = dir_name + "checker-input-" + str(test_number) + '-' + str(idx) + ".txt"
        os.system(gen_bin + " " + str(no_of_nodes) + " > " + test_case)
    
    print()
    
    for idx in range(no_of_tests):
        print("Running t-spanner on test: #", idx, flush=True)
        test_case = dir_name + "test-" + str(test_number) + '-' + str(idx) + ".txt"
        test_output = dir_name + "out-" + str(test_number) + '-' + str(idx) + ".txt"
        checker_input = dir_name + "checker-input-" + str(test_number) + '-' + str(idx) + ".txt"
        os.system(impl_bin + " " + str(t_value) + " < " + test_case + " > " + test_output)

    print()
    
    for idx in range(no_of_tests):
        info[idx] = dict()
        print("Checking test: #", idx, flush=True)
        test_case = dir_name + "test-" + str(test_number) + '-' + str(idx) + ".txt"
        test_output = dir_name + "out-" + str(test_number) + '-' + str(idx) + ".txt"
        checker_input = dir_name + "checker-input-" + str(test_number) + '-' + str(idx) + ".txt"
        os.system("echo " + str(t_value) + " > " + checker_input)
        os.system("cat " + test_case + " >> " + checker_input)
        os.system("cat " + test_output + " >> " + checker_input)
        os.system("./check < " + checker_input)
        check_output = subprocess.run("./check < " + checker_input, shell=True, capture_output=True, text=True)
        # print(check_output.stdout)
        check_output_json = (json.loads(check_output.stdout))
        info[idx]['status'] = check_output_json['status']
        info[idx]['spanner_score'] = check_output_json['spanner_score']
        info[idx]['n_value'] = no_of_nodes
        info[idx]['test_case_number'] = idx
        info[idx]['phase1_edge_count'] = check_output_json['phase1_edge_count']
        info[idx]['phase2_edge_count'] = check_output_json['phase2_edge_count']
        info[idx]['phase1_time'] = check_output_json['phase1_time']
        info[idx]['phase2_time'] = check_output_json['phase2_time']
        info[idx]['total_time'] = check_output_json['total_time']
        info[idx]['total_edges'] =  check_output_json['total_edges']
        info[idx]['original_edges'] =  check_output_json['original_edges']
        info[idx]['t_value'] = t_value
    
    metadata['outputs'] += 1
    with open('./outputs/metadata.json', 'w') as f:
        json.dump(metadata, f)  
    with open(info_json, 'w') as f:
        json.dump(info, f, indent=4)
    
    print(json.dumps(info, indent=4))

@app.command()
def ttest(impl: str, generator: str, no_of_nodes: int, no_of_tests: int, tstart=3, tend=100, tinc=10):
    tstart = max(3, int(tstart))
    tend = int(tend)
    tinc = int(tinc)
    t_values = [ i for i  in range(tstart, tend+tstart+1, tinc)]
    test_number = math.floor(time.time()) - start_time

    info = {}
    info['test_number'] = test_number
    info['cmd'] = 'ttest'
    info['impl'] = impl
    info['generator'] = generator
    info['n_value'] = no_of_nodes
    info['tstart'] = tstart
    info['tend'] = tend
    info['tinc'] = tinc
    info['no_of_tests'] = len(t_values) * no_of_tests
    info['tests_per_t'] = no_of_tests
    info['t_values'] = str(t_values)

    total_tests = len(t_values) * no_of_tests

    dir_name = "./outputs/output-" + str(test_number) + "/"
    input_dir = dir_name + "in" + "/"
    output_dir = dir_name + "out" + "/"
    checker_dir = dir_name + "check" + "/"
    os.system("mkdir " + dir_name)
    os.system(f"mkdir {input_dir}")
    os.system(f"mkdir {output_dir}")
    os.system(f"mkdir {checker_dir}")

    impl_basename = os.path.basename(impl)
    generator_basename = os.path.basename(generator)

    info_json = dir_name + "info.json"
    impl_src = dir_name + impl_basename
    gen_src = dir_name + generator_basename
    impl_bin = dir_name + "impl.out"
    gen_bin = dir_name + "generator.out"

    os.system("cp " + impl + " " + impl_src)
    os.system("cp " + generator + " " + gen_src)
    os.system("g++ " + impl_src + " -o " + impl_bin)
    os.system("g++ " + gen_src + " -o " + gen_bin)
    os.system("g++ checker.cpp -o check.out")

    print("Generating tests ... ")
    for idx in range(no_of_tests):
        print("Generating test: #", idx, flush=True)
        test_case = input_dir + "test-" + str(test_number)  + '-' + str(idx) +  ".txt"
        os.system(gen_bin + " " + str(no_of_nodes) + " > " + test_case)
    
    print()
    
    for i, t_value in enumerate(t_values):
        for idx in range(no_of_tests):
            test_num = i * no_of_tests + idx + 1
            test_case = input_dir + "test-" + str(test_number) + '-' + str(idx) + ".txt"
            test_output = output_dir + "out-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + '-' + ".txt"
            checker_input = checker_dir + "checker-input-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + ".txt"
            test_basename = os.path.basename(test_case)
            print(f"Running test: #{test_num}/{total_tests} on t = {t_value}, n = {no_of_nodes}, testcase = {idx}, path = {test_basename}", flush=True)
            os.system(impl_bin + " " + str(t_value) + " < " + test_case + " > " + test_output)

    print()
    
    i = 0
    for t_value in t_values:
        for idx in range(no_of_tests):
            info[i * no_of_tests + idx] = dict()
            test_case = input_dir + "test-" + str(test_number) + '-' + str(idx) + ".txt"
            test_output = output_dir + "out-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + '-' + ".txt"
            checker_input = checker_dir + "checker-input-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + ".txt"
            
            print(f"Checking for t: {t_value}, idx: {idx}", flush=True)
            os.system("echo " + str(t_value) + " > " + checker_input)
            os.system("cat " + test_case + " >> " + checker_input)
            os.system("cat " + test_output + " >> " + checker_input)
            # os.system("./check.out < " + checker_input)
            check_output = subprocess.run("./check.out < " + checker_input, shell=True, capture_output=True, text=True)
            # print(check_output.stdout)
            check_output_json = (json.loads(check_output.stdout))
            info[i * no_of_tests + idx]['status'] = check_output_json['status']
            info[i * no_of_tests + idx]['spanner_score'] = check_output_json['spanner_score']
            info[i * no_of_tests + idx]['n_value'] = no_of_nodes
            info[i * no_of_tests + idx]['test_case_number'] = idx
            info[i * no_of_tests + idx]['phase1_edge_count'] = check_output_json['phase1_edge_count']
            info[i * no_of_tests + idx]['phase2_edge_count'] = check_output_json['phase2_edge_count']
            info[i * no_of_tests + idx]['phase1_time'] = check_output_json['phase1_time']
            info[i * no_of_tests + idx]['phase2_time'] = check_output_json['phase2_time']
            info[i * no_of_tests + idx]['total_time'] = check_output_json['total_time']
            info[i * no_of_tests + idx]['total_edges'] =  check_output_json['total_edges']
            info[i * no_of_tests + idx]['original_edges'] =  check_output_json['original_edges']
            info[i * no_of_tests + idx]['t_value'] = t_value
        i += 1

    #os.system('rm ' + dir_name + 'out-*')
    #os.system('rm ' + dir_name + 'checker-input-*')

 
    with open(info_json, 'w') as f:
        json.dump(info, f, indent=4)
    
    print(json.dumps(info, indent=4))

@app.command()
def ntest(impl: str, generator: str, t_value: int, no_of_tests: int, nstart=3, nend=100, ninc=10):
    nstart = max(3, int(nstart))
    nend = int(nend)
    ninc = int(ninc)
    n_values = [ i for i  in range(nstart, nend+1, ninc)]
    test_number = math.floor(time.time()) - start_time
    info = {}
    info['cmd'] = 'ntest'
    info['nstart'] = nstart
    info['nend'] = nend
    info['ninc'] = ninc
    # info['n_value'] = no_of_nodes
    info['test_number'] = test_number
    info['impl'] = impl
    info['generator'] = generator
    info['t_value'] = t_value
    info['no_of_tests'] = len(n_values) * no_of_tests
    info['tests_per_n'] = no_of_tests
    # no_of_tests = len(t_values)
    info['n_values'] = str(n_values)
    
    total_tests = len(n_values) * no_of_tests

    dir_name = "./outputs/output-" + str(test_number) + "/"
    input_dir = dir_name + "in" + "/"
    output_dir = dir_name + "out" + "/"
    checker_dir = dir_name + "check" + "/"
    os.system("mkdir " + dir_name)
    os.system(f"mkdir {input_dir}")
    os.system(f"mkdir {output_dir}")
    os.system(f"mkdir {checker_dir}")

    impl_basename = os.path.basename(impl)
    generator_basename = os.path.basename(generator)

    info_json = dir_name + "info.json"
    impl_src = dir_name + impl_basename
    gen_src = dir_name + generator_basename
    impl_bin = dir_name + "impl.out"
    gen_bin = dir_name + "generator.out"

    os.system("cp " + impl + " " + impl_src)
    os.system("cp " + generator + " " + gen_src)
    os.system("g++ " + impl_src + " -o " + impl_bin)
    os.system("g++ " + gen_src + " -o " + gen_bin)
    os.system("g++ checker.cpp -o check.out")

    print("Generating tests ... ")
    for no_of_nodes in n_values:
        for idx in range(no_of_tests):
            print("Generating test: #", idx, flush=True)
            test_case = input_dir + "test-" + str(test_number)  + '-' + str(no_of_nodes) + '-' + str(idx)  +  ".txt"
            os.system(gen_bin + " " + str(no_of_nodes) + " > " + test_case)
    
    print()
    
    for i, no_of_nodes in enumerate(n_values):
        for idx in range(no_of_tests):
            test_num = i * no_of_tests + idx + 1
            test_case = input_dir + "test-" + str(test_number)  + '-' + str(no_of_nodes) + '-' + str(idx)  +  ".txt"
            test_output = output_dir + "out-" + str(test_number) + '-' + str(no_of_nodes) + '-' + str(idx) + '-' + ".txt"
            checker_input = checker_dir + "checker-input-" + str(test_number) + '-' + str(no_of_nodes) + '-' + str(idx) + ".txt"
            test_basename = os.path.basename(test_case)
            print(f"Running test: #{test_num}/{total_tests} on t = {t_value}, n = {i}, testcase = {idx}, path = {test_basename}", flush=True)
            os.system(impl_bin + " " + str(t_value) + " < " + test_case + " > " + test_output)

    print()
    
    i = 0
    for no_of_nodes in n_values:
        for idx in range(no_of_tests):
            info[i * no_of_tests + idx] = dict()
            test_case = input_dir + "test-" + str(test_number)  + '-' + str(no_of_nodes) + '-' + str(idx)  +  ".txt"
            test_output = output_dir + "out-" + str(test_number) + '-' + str(no_of_nodes) + '-' + str(idx) + '-' + ".txt"
            checker_input = checker_dir + "checker-input-" + str(test_number) + '-' + str(no_of_nodes) + '-' + str(idx) + ".txt"
            
            print("Checking for k: #", t_value, flush=True)
            os.system("echo " + str(t_value) + " > " + checker_input)
            os.system("cat " + test_case + " >> " + checker_input)
            os.system("cat " + test_output + " >> " + checker_input)
            # os.system("./check.out < " + checker_input)
            check_output = subprocess.run("./check.out < " + checker_input, shell=True, capture_output=True, text=True)
            # print(check_output.stdout)
            check_output_json = (json.loads(check_output.stdout))
            info[i * no_of_tests + idx]['status'] = check_output_json['status']
            info[i * no_of_tests + idx]['spanner_score'] = check_output_json['spanner_score']
            info[i * no_of_tests + idx]['n_value'] = no_of_nodes
            info[i * no_of_tests + idx]['test_case_number'] = idx
            info[i * no_of_tests + idx]['phase1_edge_count'] = check_output_json['phase1_edge_count']
            info[i * no_of_tests + idx]['phase2_edge_count'] = check_output_json['phase2_edge_count']
            info[i * no_of_tests + idx]['phase1_time'] = check_output_json['phase1_time']
            info[i * no_of_tests + idx]['phase2_time'] = check_output_json['phase2_time']
            info[i * no_of_tests + idx]['total_time'] = check_output_json['total_time']
            info[i * no_of_tests + idx]['total_edges'] =  check_output_json['total_edges']
            info[i * no_of_tests + idx]['original_edges'] =  check_output_json['original_edges']
            info[i * no_of_tests + idx]['t_value'] = t_value

        i += 1

    #os.system('rm ' + dir_name + 'out-*')
    #os.system('rm ' + dir_name + 'checker-input-*')
    with open(info_json, 'w') as f:
        json.dump(info, f, indent=4)
    
    print(json.dumps(info, indent=4))

@app.command()
def ttest_data(impl: str, dataset_path : str, no_of_nodes: int, tstart=3, tend=100, tinc=10):
    tstart = max(3, int(tstart))
    tend = int(tend)
    tinc = int(tinc)
    t_values = [ i for i  in range(tstart, tend+tstart+1, tinc)]
    test_number = math.floor(time.time()) - start_time

    info = {}
    info['test_number'] = test_number
    info['cmd'] = 'ttest-data'
    info['tstart'] = tstart
    info['tend'] = tend
    info['tinc'] = tinc
    info['impl'] = impl
    info['dataset_path'] = dataset_path
    info['n_value'] = no_of_nodes
    info['t_values'] = str(t_values)

    if dataset_path[-1] != '/':
        dataset_path += '/'

    dir_name = "./outputs/output-" + str(test_number) + "/"
    output_dir = dir_name + "out" + "/"
    checker_dir = dir_name + "check" + "/"
    test_dataset_path = dir_name + "dataset" + "/"
    os.system("mkdir " + dir_name)
    os.system(f"mkdir {test_dataset_path}")
    os.system(f"mkdir {output_dir}")
    os.system(f"mkdir {checker_dir}")

    # copying all the testcases from dataset directory to output directory
    os.system(f"cp {dataset_path}*.txt {test_dataset_path}")

    impl_basename = os.path.basename(impl)
    info_json = dir_name + "info.json"
    impl_src = dir_name + impl_basename
    impl_bin = dir_name + "impl.out"

    # copying and compiling the implementation file and checker file
    os.system("cp " + impl + " " + impl_src)
    os.system("g++ " + impl_src + " -o " + impl_bin)
    os.system("g++ checker.cpp -o check.out")

    # listing all the testcases in the testcase directory
    testcase_filepaths = []
    for filepath in os.listdir(test_dataset_path):
        if filepath.endswith(".txt"):
            testcase_filepaths.append(filepath)

    no_of_tests = len(testcase_filepaths)
    info['no_of_tests'] = len(t_values) * no_of_tests
    info['tests_per_t'] = no_of_tests

    total_tests = len(t_values) * len(testcase_filepaths)

    # generating the output for all the input testcases
    for i, t_value in enumerate(t_values):
        for idx, filepath in enumerate(testcase_filepaths):
            test_num = i * no_of_tests + idx + 1
            print(f"Running test: #{test_num}/{total_tests} with t = {t_value}, n = {no_of_nodes}, testcase: #{idx}, path = {filepath}", flush=True)
            in_path = test_dataset_path + filepath
            out_path = output_dir + "out-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + '-' + ".txt"
            os.system(impl_bin + " " + str(t_value) + " < " + in_path + " > " + out_path)

    print()
    
    for i, t_value in enumerate(t_values):
        for idx, filepath in enumerate(testcase_filepaths):
            info[i * no_of_tests + idx] = dict()
            in_path = test_dataset_path + filepath
            out_path = output_dir + "out-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + '-' + ".txt"
            checker_input = checker_dir + "checker-input-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + ".txt"
            
            print(f"Checking for t: {t_value}, idx: {idx}", flush=True)
            os.system("echo " + str(t_value) + " > " + checker_input)
            os.system("cat " + in_path + " >> " + checker_input)
            os.system("cat " + out_path + " >> " + checker_input)
            # os.system("./check.out < " + checker_input)
            check_output = subprocess.run("./check.out < " + checker_input, shell=True, capture_output=True, text=True)
            # print(check_output.stdout)
            check_output_json = (json.loads(check_output.stdout))
            info[i * no_of_tests + idx]['status'] = check_output_json['status']
            info[i * no_of_tests + idx]['spanner_score'] = check_output_json['spanner_score']
            info[i * no_of_tests + idx]['n_value'] = no_of_nodes
            info[i * no_of_tests + idx]['test_case_number'] = idx
            info[i * no_of_tests + idx]['phase1_edge_count'] = check_output_json['phase1_edge_count']
            info[i * no_of_tests + idx]['phase2_edge_count'] = check_output_json['phase2_edge_count']
            info[i * no_of_tests + idx]['phase1_time'] = check_output_json['phase1_time']
            info[i * no_of_tests + idx]['phase2_time'] = check_output_json['phase2_time']
            info[i * no_of_tests + idx]['total_time'] = check_output_json['total_time']
            info[i * no_of_tests + idx]['total_edges'] =  check_output_json['total_edges']
            info[i * no_of_tests + idx]['original_edges'] =  check_output_json['original_edges']
            info[i * no_of_tests + idx]['t_value'] = t_value

    #os.system(f'rm -r {output_dir}')
    #os.system(f'rm -r {checker_dir}')
 
    with open(info_json, 'w') as f:
        json.dump(info, f, indent=4)
    
    print(json.dumps(info, indent=4))

@app.command()
def test_data(impl: str, dataset_path : str, t_value: int):
    test_number = math.floor(time.time()) - start_time
    info = {}
    info['cmd'] = 'test-data'
    # info['n_value'] = no_of_nodes
    info['test_number'] = test_number
    info['impl'] = impl
    info['dataset_path'] = dataset_path
    info['t_value'] = t_value

    if dataset_path[-1] != '/':
        dataset_path += '/'

    dir_name = "./outputs/output-" + str(test_number) + "/"
    output_dir = dir_name + "out" + "/"
    checker_dir = dir_name + "check" + "/"
    test_dataset_path = dir_name + "dataset" + "/"
    os.system("mkdir " + dir_name)
    os.system(f"mkdir {test_dataset_path}")
    os.system(f"mkdir {output_dir}")
    os.system(f"mkdir {checker_dir}")

    # copying all the testcases from dataset directory to output directory
    os.system(f"cp {dataset_path}*.txt {test_dataset_path}")

    impl_basename = os.path.basename(impl)
    info_json = dir_name + "info.json"
    impl_src = dir_name + impl_basename
    impl_bin = dir_name + "impl.out"

    # copying all the testcases from dataset directory to output directory
    os.system(f"cp {dataset_path}*.txt {test_dataset_path}")
    os.system("cp " + impl + " " + impl_src)
    os.system("g++ " + impl_src + " -o " + impl_bin)
    os.system("g++ checker.cpp -o check.out")

    # listing all the testcases in the testcase directory
    testcase_filepaths = []
    for filepath in os.listdir(test_dataset_path):
        if filepath.endswith(".txt"):
            testcase_filepaths.append(filepath)

    n_values = []
    n_values_raw = []
    no_of_tests = len(testcase_filepaths)
    info['no_of_tests'] = no_of_tests

    # generating the output for all the input testcases
    for idx, filepath in enumerate(testcase_filepaths):
        test_num = idx + 1
        in_path = test_dataset_path + filepath

        f = open(in_path, 'r')
        n_value = int(f.readline().split(' ')[0])
        n_values_raw.append(n_value)
        if n_value not in n_values:
            n_values.append(n_value)

        out_path = output_dir + "out-" + str(test_number) + '-' + str(n_value) + '-' + str(idx) + '-' + ".txt"
        print(f"Running test: #{test_num}/{no_of_tests} with t = {t_value}, n = {n_value}, path = {filepath}", flush=True)
        os.system(impl_bin + " " + str(t_value) + " < " + in_path + " > " + out_path)

    print()

    info['n_values_raw'] = str(n_values_raw)
    info['n_values'] = str(n_values)
    info['tests_per_n'] = no_of_tests/len(n_values)
    
    for idx, filepath in enumerate(testcase_filepaths):
        info[idx] = dict()
        in_path = test_dataset_path + filepath
        f = open(in_path, 'r')
        n_value = int(f.readline().split(' ')[0])
        out_path = output_dir + "out-" + str(test_number) + '-' + str(n_value) + '-' + str(idx) + '-' + ".txt"
        checker_input = checker_dir + "checker-input-" + str(test_number) + '-' + str(n_value) + '-' + str(idx) + ".txt"
        
        print("Checking test: #{idx + 1}{no_of_tests} with t = {t_value}, n = {n_value}, path = {out_path}")
        os.system("echo " + str(t_value) + " > " + checker_input)
        os.system("cat " + in_path + " >> " + checker_input)
        os.system("cat " + out_path + " >> " + checker_input)
        # os.system("./check.out < " + checker_input)
        check_output = subprocess.run("./check.out < " + checker_input, shell=True, capture_output=True, text=True)
        # print(check_output.stdout)
        check_output_json = (json.loads(check_output.stdout))
        info[idx]['status'] = check_output_json['status']
        info[idx]['spanner_score'] = check_output_json['spanner_score']
        info[idx]['n_value'] = check_output_json['n_value']
        info[idx]['test_case_number'] = idx
        info[idx]['phase1_edge_count'] = check_output_json['phase1_edge_count']
        info[idx]['phase2_edge_count'] = check_output_json['phase2_edge_count']
        info[idx]['phase1_time'] = check_output_json['phase1_time']
        info[idx]['phase2_time'] = check_output_json['phase2_time']
        info[idx]['total_time'] = check_output_json['total_time']
        info[idx]['total_edges'] =  check_output_json['total_edges']
        info[idx]['original_edges'] =  check_output_json['original_edges']
        info[idx]['t_value'] = check_output_json['t_value']

    #os.system('rm ' + dir_name + 'out-*')
    #os.system('rm ' + dir_name + 'checker-input-*')
    with open(info_json, 'w') as f:
        json.dump(info, f, indent=4)
    
    print(json.dumps(info, indent=4))

@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
