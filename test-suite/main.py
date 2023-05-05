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
    info['cmd'] = 'cross_t_test'
    info['impl'] = impl
    info['generator'] = generator
    info['n_value'] = no_of_nodes
    # info['t_value'] = t_value
    info['no_of_tests'] = len(t_values) * no_of_tests
    info['tests_per_t'] = no_of_tests
    # no_of_tests = len(t_values)
    info['t_values'] = str(t_values)
    dir_name = "./outputs/output-" + str(test_number) + "/"
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
    os.system("g++ checker.cpp -o check.out")

    print("Generating tests ... ")
    for idx in range(no_of_tests):
        print("Generating test: #", idx, flush=True)
        test_case = dir_name + "test-" + str(test_number)  + '-' + str(idx) +  ".txt"
        os.system(gen_bin + " " + str(no_of_nodes) + " > " + test_case)
    
    print()
    
    for t_value in t_values:
        for idx in range(no_of_tests):
            print(f"Running t-spanner on t = {t_value}, n = {no_of_nodes}, test: # {idx}", flush=True)
            test_case = dir_name + "test-" + str(test_number) + '-' + str(idx) + ".txt"
            test_output = dir_name + "out-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + '-' + ".txt"
            checker_input = dir_name + "checker-input-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + ".txt"
            os.system(impl_bin + " " + str(t_value) + " < " + test_case + " > " + test_output)

    print()
    
    i = 0
    for t_value in t_values:
        for idx in range(no_of_tests):
            info[i * no_of_tests + idx] = dict()
            test_case = dir_name + "test-" + str(test_number) + '-' + str(idx) + ".txt"
            test_output = dir_name + "out-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + '-' + ".txt"
            checker_input = dir_name + "checker-input-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + ".txt"
            
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

    os.system('rm ' + dir_name + 'out-*')
    os.system('rm ' + dir_name + 'checker-input-*')

 
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
    info['cmd'] = 'cross_n_test'
    # info['n_value'] = no_of_nodes
    info['test_number'] = test_number
    info['impl'] = impl
    info['generator'] = generator
    info['t_value'] = t_value
    info['no_of_tests'] = len(n_values) * no_of_tests
    info['tests_per_n'] = no_of_tests
    # no_of_tests = len(t_values)
    info['n_values'] = str(n_values)
    dir_name = "./outputs/output-" + str(test_number) + "/"
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
    os.system("g++ checker.cpp -o check.out")

    print("Generating tests ... ")
    for no_of_nodes in n_values:
        for idx in range(no_of_tests):
            print("Generating test: #", idx, flush=True)
            test_case = dir_name + "test-" + str(test_number)  + '-' + str(no_of_nodes) + '-' + str(idx)  +  ".txt"
            os.system(gen_bin + " " + str(no_of_nodes) + " > " + test_case)
    
    print()
    
    for no_of_nodes in n_values:
        for idx in range(no_of_tests):
            print(f"Running t-spanner on n = {no_of_nodes}, t = {t_value}, test: #{idx}", flush=True)
            test_case = dir_name + "test-" + str(test_number)  + '-' + str(no_of_nodes) + '-' + str(idx)  +  ".txt"
            test_output = dir_name + "out-" + str(test_number) + '-' + str(no_of_nodes) + '-' + str(idx) + '-' + ".txt"
            checker_input = dir_name + "checker-input-" + str(test_number) + '-' + str(no_of_nodes) + '-' + str(idx) + ".txt"
            os.system(impl_bin + " " + str(t_value) + " < " + test_case + " > " + test_output)

    print()
    
    i = 0
    for no_of_nodes in n_values:
        for idx in range(no_of_tests):
            info[i * no_of_tests + idx] = dict()
            test_case = dir_name + "test-" + str(test_number)  + '-' + str(no_of_nodes) + '-' + str(idx)  +  ".txt"
            test_output = dir_name + "out-" + str(test_number) + '-' + str(no_of_nodes) + '-' + str(idx) + '-' + ".txt"
            checker_input = dir_name + "checker-input-" + str(test_number) + '-' + str(no_of_nodes) + '-' + str(idx) + ".txt"
            
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

    os.system('rm ' + dir_name + 'out-*')
    os.system('rm ' + dir_name + 'checker-input-*')
    with open(info_json, 'w') as f:
        json.dump(info, f, indent=4)
    
    print(json.dumps(info, indent=4))

@app.command()
def ttestdata(impl: str, dataset_path : str, no_of_nodes: int, tstart=3, tend=100, tinc=10):
    tstart = max(3, int(tstart))
    tend = int(tend)
    tinc = int(tinc)
    t_values = [ i for i  in range(tstart, tend+tstart+1, tinc)]
    test_number = math.floor(time.time()) - start_time

    info = {}
    info['test_number'] = test_number
    info['cmd'] = 'ttestdata'
    info['impl'] = impl
    info['dataset_path'] = dataset_path
    info['n_value'] = no_of_nodes
    info['t_values'] = str(t_values)

    if dataset_path[-1] != '/':
        dataset_path += '/'

    dir_name = "./outputs/output-" + str(test_number) + "/"
    dataset_basename = os.path.basename(dataset_path)
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

    # generating the output for all the input testcases
    for i, t_value in enumerate(t_values):
        for idx, filepath in enumerate(testcase_filepaths):
            test_num = i * no_of_tests + idx + 1
            print(f"Running test: #{test_num} with t = {t_value}, n = {no_of_nodes}, testcase: #{idx}, path = {filepath}", flush=True)
            in_path = test_dataset_path + filepath
            out_path = output_dir + "out-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + '-' + ".txt"
            os.system(impl_bin + " " + str(t_value) + " < " + in_path + " > " + out_path)

    print()
    
    i = 0
    for t_value in t_values:
        for idx, filepath in enumerate(testcase_filepaths):
            info[i * no_of_tests + idx] = dict()
            in_path = test_dataset_path + filepath
            out_path = dir_name + "out-" + str(test_number) + '-' + str(t_value) + '-' + str(idx) + '-' + ".txt"
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
        i += 1

    os.system(f'rm -r {output_dir}')
    os.system(f'rm -r {checker_dir}')
 
    with open(info_json, 'w') as f:
        json.dump(info, f, indent=4)
    
    print(json.dumps(info, indent=4))

@app.command()
def ntestdata(impl: str, dataset_dir: str, t_value: int):
    # n_values = [ i for i  in range(nstart, nend+1, ninc)]
    test_number = math.floor(time.time()) - start_time
    info = {}
    info['cmd'] = 'ntestdata'
    # info['n_value'] = no_of_nodes
    info['test_number'] = test_number
    info['impl'] = impl
    # info['generator'] = generator
    info['t_value'] = t_value
    # info['tests_per_n'] = no_of_tests
    # no_of_tests = len(t_values)
    # info['n_values'] = str(n_values)
    dir_name = "./outputs/output-" + str(test_number) + "/"
    os.system("mkdir " + dir_name)

    impl_basename = os.path.basename(impl)
    # generator_basename = os.path.basename(generator)

    info_json = dir_name + "info.json"
    impl_src = dir_name + impl_basename
    # gen_src = dir_name + generator_basename
    impl_bin = dir_name + "impl.out"
    # gen_bin = dir_name + "generator.out"

    os.system("cp " + impl + " " + impl_src)

    # os.system("cp " + generator + " " + gen_src)
    os.system("g++ " + impl_src + " -o " + impl_bin)
    # os.system("g++ " + gen_src + " -o " + gen_bin)
    os.system("g++ checker.cpp -o check.out")

    print("Copying tests ... ")
    # for no_of_nodes in n_values:
    #     for idx in range(no_of_tests):
    #         print("Generating test: #", idx, flush=True)
    #         test_case = dir_name + "test-" + str(test_number)  + '-' + str(no_of_nodes) + '-' + str(idx)  +  ".txt"
    #         os.system(gen_bin + " " + str(no_of_nodes) + " > " + test_case)
    test_names = [f for f in os.listdir(dataset_dir) if os.path.isfile(os.path.join(dataset_dir, f))]
    for test_name in test_names:
        print("Copying test: ", test_name, flush=True)
        os.system("cp " + dataset_dir + "/" + test_name + " " + dir_name)
    info['no_of_tests'] = len(test_names)
    

    print()
    
    for test_name in test_names:
        print(f"Running t-spanner on test: #{test_name}", flush=True)
        test_case = dir_name + test_name
        test_output = dir_name + "out-" + str(test_number) + '-' + test_name
        checker_input = dir_name + "checker-input-" + str(test_number) + '-' + test_name
        os.system(impl_bin + " " + str(t_value) + " < " + test_case + " > " + test_output)

    print()
    
    i = 0
    for test_name in test_names:
        info[i] = dict()
        test_case = dir_name + test_name
        test_output = dir_name + "out-" + str(test_number) + '-' + test_name
        checker_input = dir_name + "checker-input-" + str(test_number) + '-' + test_name
       
        print("Checking for k: #", t_value, flush=True)
        os.system("echo " + str(t_value) + " > " + checker_input)
        os.system("cat " + test_case + " >> " + checker_input)
        os.system("cat " + test_output + " >> " + checker_input)
        # os.system("./check.out < " + checker_input)
        check_output = subprocess.run("./check.out < " + checker_input, shell=True, capture_output=True, text=True)
        # print(check_output.stdout)
        check_output_json = (json.loads(check_output.stdout))
        info[i]['status'] = check_output_json['status']
        info[i]['spanner_score'] = check_output_json['spanner_score']
        info[i]['n_value'] = check_output_json['no_of_nodes']
        info[i]['test_case_number'] = i
        info[i]['test_name'] = test_case
        info[i]['phase1_edge_count'] = check_output_json['phase1_edge_count']
        info[i]['phase2_edge_count'] = check_output_json['phase2_edge_count']
        info[i]['phase1_time'] = check_output_json['phase1_time']
        info[i]['phase2_time'] = check_output_json['phase2_time']
        info[i]['total_time'] = check_output_json['total_time']
        info[i]['total_edges'] =  check_output_json['total_edges']
        info[i]['original_edges'] =  check_output_json['original_edges']
        info[i]['t_value'] = t_value

        i += 1

    os.system('rm ' + dir_name + 'out-*')
    os.system('rm ' + dir_name + 'checker-input-*')
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
