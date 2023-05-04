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
        json.dump(info, f)
    
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
