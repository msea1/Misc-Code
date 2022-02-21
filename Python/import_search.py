import sys
from os import getcwd
from pathlib import Path
from re import compile, findall

IMPORT_PATTERN = compile(r'^import (.*)$')
FROM_PATTERN = compile(r'^from (.*?)[. ].*$')


def get_imports(dir_head: str):
    all_files = set(Path(dir_head).rglob("*.py"))
    test_files = set(Path(dir_head).rglob("*test*.py"))
    code_files = all_files - test_files
    imports = set(sys.builtin_module_names)
    code_imports = set()
    for py_file in code_files:
        code_imports.update(get_imports_from_python_file(str(py_file)))
    code_imports -= imports
    print('IMPORTS IN CODE FILES:')
    print("\n".join(sorted(code_imports)))

    new_imports = set()
    for py_file in test_files:
        new_imports.update(get_imports_from_python_file(str(py_file)))
    new_imports -= imports
    new_imports -= code_imports
    print('\n\nIMPORTS IN TEST FILES:')
    print("\n".join(sorted(new_imports)))


def get_imports_from_python_file(py_file: str) -> set:
    matches = set()
    with open(py_file) as fin:
        for text_line in fin.readlines():
            text_line = text_line.strip()
            matches.update(set(findall(IMPORT_PATTERN, text_line)))
            matches.update(set(findall(FROM_PATTERN, text_line)))
    return matches


if __name__ == '__main__':
    dir_head = getcwd()
    if len(sys.argv) == 2:
        dir_head = sys.argv[1]
    print(f'Checking imports at {dir_head}')
    get_imports(dir_head)

