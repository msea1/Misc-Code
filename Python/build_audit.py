from glob import iglob
from importlib import import_module
from inspect import getmembers, getmodulename, isclass, ismodule
from os.path import join, split
from re import findall

GEMINI_ROOT = '/home/mcarruth/Code/gemini/'


def get_3rd_party_list():
    with open(join(GEMINI_ROOT, '3rdparty/BUILD')) as fin:
        outside_info_blob = fin.read()
    matches = findall('.*name=\'(.*)\',.*', outside_info_blob)
    return set([ma.lower() for ma in matches])


def get_service_build(service_path):
    with open(join(GEMINI_ROOT, service_path, 'BUILD')) as fin:
        outside_info_blob = fin.read()
    defs = outside_info_blob.split('\n\n')
    code_def = [x for x in defs if 'python_library' in x][0]
    test_def = [x for x in defs if 'python_tests' in x][0]
    code_matches = set([x.lower() for x in findall(' {2}\'(.*)\',', code_def)])
    test_matches = set([x.lower() for x in findall(' {2}\'(.*)\',', test_def)])
    return code_matches, test_matches


def pyfiles(service_path, service_name):
    top_pys = list(iglob(join(GEMINI_ROOT, service_path, '*.py')))
    code_pys = list(iglob(join(GEMINI_ROOT, service_path, service_name, '**/*.py'), recursive=True))
    test_pys = list(iglob(join(GEMINI_ROOT, service_path, f'tests_{service_name}', '**/*.py'), recursive=True))
    top_pys.extend(code_pys)
    return top_pys, test_pys


def built_in(module_origin):
    return '/usr/lib/python3' in module_origin or 'built-in' in module_origin


test_service = 'obscura'
test_service = 'obscura_workflow'
path_there = 'services/imaging-services/obscura'
path_there = 'libraries/obscura-workflow'
imports_founds = set()

code_files, _ = pyfiles(path_there, test_service)
for cf in code_files:
    module_name = getmodulename(cf)
    prefix = '.'.join(split(cf.split(test_service)[-1])[:-1]).replace('/', '')
    module_path = test_service if not prefix else '.'.join([test_service, prefix])
    try:
        exam = import_module(f'{module_path}.{module_name.lower()}')
        m = getmembers(exam)

        # classes
        c1 = [x[1].__module__.split('.')[0] for x in filter(lambda x: isclass(x[1]), m)]
        c1 = set(c1)
        bi = set()
        for c in c1:
            try:
                if not built_in(repr(import_module(c))):
                    bi.add(c)
            except Exception as e:
                print(f'{e} on {c} in class to module')

        try:
            bi.remove(test_service)
        except KeyError:
            pass

        m1 = [x[1].__name__.split('.')[0] for x in filter(lambda x: ismodule(x[1]), m) if not built_in(str(x[1]))]
        m1 = set(m1)

        imports_founds = imports_founds | bi | m1
    except ModuleNotFoundError:
        # try manual scan
        with open(cf) as read_f:
            contents = read_f.readlines()
            froms = [f.split('from ')[1].split(' ')[0].split('.')[0].replace('\n', '') for f in contents if f.startswith('from')]
            imports = [i.split(' ')[1].replace('\n', '') for i in contents if i.startswith('import')]
            froms.extend(imports)
            pruned = set()
            for f in froms:
                try:
                    if not built_in(repr(import_module(f))):
                        pruned.add(f)
                except Exception as e:
                    print(f'{e} on {f}')
            imports_founds = imports_founds | set(pruned)

third_party = get_3rd_party_list()
this_code, _ = get_service_build(path_there)
extra = set()
missing = set(imports_founds)
for in_code in imports_founds:
    in_build = in_code.replace('_', '-').lower()
    if in_build in third_party:
        if f'3rdparty:{in_build}' in this_code:
            missing.remove(in_code)
            this_code.remove(f'3rdparty:{in_build}')
    elif f'libraries/{in_build}' in this_code:
        missing.remove(in_code)
        this_code.remove(f'libraries/{in_build}')
    elif f'libraries/{in_code}' in this_code:
        missing.remove(in_code)
        this_code.remove(f'libraries/{in_code}')

print(f'missing: {sorted(missing)}')
print(f'extra: {sorted(this_code)}')
