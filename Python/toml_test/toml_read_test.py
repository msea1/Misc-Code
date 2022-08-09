import glob
import timeit
from os.path import basename, splitext
from typing import Dict, List

N_RUNS = 100


def test_tomli_load(file_path: str):
    return timeit.timeit(
        setup=f"import tomli",
        stmt=f"with open('{file_path}', 'rb') as r: tomli.load(r)",
        number=N_RUNS
    )


def test_toml_load(file_path: str):
    return timeit.timeit(
        setup=f"import toml",
        stmt=f"with open('{file_path}') as r: toml.load(r)",
        number=N_RUNS
    )


def test_json_load(file_path: str):
    return timeit.timeit(
        setup=f"import json",
        stmt=f"with open('{file_path}') as r: json.load(r)",
        number=N_RUNS
    )


def main():
    results: Dict[str, List[float, float]] = {}
    for test_file in glob.glob('samples/**', recursive=True):
        prefix_name = splitext(basename(test_file))[0]
        if not prefix_name:
            continue
        if prefix_name not in results:
            results[prefix_name] = [0, 0, 0]
        if test_file.endswith("toml"):
            results[prefix_name][0] = test_toml_load(test_file) / N_RUNS * 1000
            results[prefix_name][1] = test_tomli_load(test_file) / N_RUNS * 1000
        elif test_file.endswith("json"):
            results[prefix_name][2] = test_json_load(test_file) / N_RUNS * 1000

    print(" ~~~~~~~~~~~~~ TEST REPORT ~~~~~~~~~~~~~ ")
    print("FILE NAME\t\t\tTOML LOAD TIME\tTOMLI LOAD TIME\tJSON LOAD TIME")
    for k, v in results.items():
        print('{:<22}{:>2.2f}ms\t\t{:>2.2f}ms\t\t{:>2.2f}ms'.format(k, v[0], v[1], v[2]), sep='')


if __name__ == "__main__":
    main()
