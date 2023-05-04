import typer
import os
import json
# import timer
import tqdm
import subprocess


app = typer.Typer()


@app.command()
def doTest(impl: str, generator: str, no_of_nodes: int, t_value: int):
    with open("./outputs/metadata.json", "r") as f:
        metadata = json.load(f)
    test_number = metadata['outputs']
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
    test_number = metadata['outputs']
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
def ttest(impl: str, generator: str, no_of_nodes: int, no_of_tests: int, nstart=3, nend=100, ninc=10):
    nstart = max(3, int(nstart))
    nend = int(nend)
    ninc = int(ninc)
    t_values = [ i for i  in range(nstart, nend+nstart+1, ninc)]
    with open("./outputs/metadata.json", "r") as f:
        metadata = json.load(f)
    test_number = metadata['outputs']
    info = {}
    info['cmd'] = 'cross_t_test'
    info['impl'] = impl
    info['generator'] = generator
    info['n_value'] = no_of_nodes
    # info['t_value'] = t_value
    info['no_of_tests'] = len(t_values) * no_of_tests
    info['tests_per_t'] = no_of_tests
    # no_of_tests = len(t_values)
    info['t_values'] = str(t_values)
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
        test_case = dir_name + "test-" + str(test_number)  + '-' + str(idx) +  ".txt"
        os.system(gen_bin + " " + str(no_of_nodes) + " > " + test_case)
    
    print()
    
    for t_value in t_values:
        for idx in range(no_of_tests):
            print("Running t-spanner on test: #", idx, flush=True)
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
            
            print("Checking for t: ", t_value, " idx: ", idx, flush=True)
            os.system("echo " + str(t_value) + " > " + checker_input)
            os.system("cat " + test_case + " >> " + checker_input)
            os.system("cat " + test_output + " >> " + checker_input)
            os.system("./check < " + checker_input)
            check_output = subprocess.run("./check < " + checker_input, shell=True, capture_output=True, text=True)
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

    metadata['outputs'] += 1

    os.system('rm ' + dir_name + 'out-*')
    os.system('rm ' + dir_name + 'checker-input-*')

    with open('./outputs/metadata.json', 'w') as f:
        json.dump(metadata, f)  
    with open(info_json, 'w') as f:
        json.dump(info, f, indent=4)
    
    print(json.dumps(info, indent=4))

@app.command()
def ntest(impl: str, generator: str, t_value: int, no_of_tests: int, nstart=3, nend=100, ninc=10):
    nstart = max(3, int(nstart))
    nend = int(nend)
    ninc = int(ninc)
    n_values = [ i for i  in range(nstart, nend+1, ninc)]
    with open("./outputs/metadata.json", "r") as f:
        metadata = json.load(f)
    test_number = metadata['outputs']
    info = {}
    info['cmd'] = 'cross_t_test'
    # info['n_value'] = no_of_nodes
    info['t_value'] = t_value
    info['no_of_tests'] = len(n_values) * no_of_tests
    info['tests_per_n'] = no_of_tests
    # no_of_tests = len(t_values)
    info['n_values'] = str(n_values)
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
            print("Running t-spanner on test: #", idx, flush=True)
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

    metadata['outputs'] += 1
    os.system('rm ' + dir_name + 'out-*')
    os.system('rm ' + dir_name + 'checker-input-*')
    with open('./outputs/metadata.json', 'w') as f:
        json.dump(metadata, f)  
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
