import typer
import os
import json
# import timer
import tqdm


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
    info_json = dir_name + "info.json"
    impl_src = dir_name + impl
    gen_src = dir_name + generator
    impl_bin = dir_name + "impl"
    gen_bin = dir_name + "generator"
    test_case = dir_name + "test-" + str(test_number) + ".txt"
    test_output = dir_name + "out-" + str(test_number) + ".txt"
    checker_input = dir_name + "checker-input-" + str(test_number) + ".txt"
    with tqdm.tqdm(total=70) as pbar:
        os.system("cp " + impl + " " + dir_name)
        pbar.update(10)
        os.system("cp " + generator + " " + dir_name)
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
        pbar.update(10)
    metadata['outputs'] += 1
    with open('./outputs/metadata.json', 'w') as f:
        json.dump(metadata, f)  
    with open(info_json, 'w') as f:
        json.dump(info, f)

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