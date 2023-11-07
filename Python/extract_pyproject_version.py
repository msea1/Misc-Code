new file mode 100755
@@ -0,0 +1,41 @@
#!/usr/bin/env python3

import sys
import tomllib


def sanitize_version(toml_val: str | dict) -> str:
    if isinstance(toml_val, str):
        return toml_val
    if isinstance(toml_val, dict):
        return toml_val["version"]


def _get_caret_max_version_str(version_str: str) -> str:
    # strip off leading '^', then break into major.minor.patch
    parts = version_str[1:].split('.')
    if parts[0] != '0':
        return f"{int(parts[0])+1}.0.0"
    elif parts[1] != '0':
        return f"0.{int(parts[1]) + 1}.0"
    return f"0.0.{int(parts[2]) + 1}"


def de_poetry_version_str(version_str: str) -> str:
    if version_str.startswith("^"):
        max_ver = _get_caret_max_version_str(version_str)
        return f" >={version_str[1:]}, <{max_ver}"
    else:
        return f' =={version_str}'


package_name = sys.argv[1]

with open("pyproject.toml", "rb") as f:
    reqs = tomllib.load(f)

if reqs:
    if main := reqs["tool"]["poetry"]["dependencies"].get(package_name):
        print(package_name + de_poetry_version_str(sanitize_version(main)))
    elif dev := reqs["tool"]["poetry"]["group"]["dev"]["dependencies"].get(package_name):
        print(package_name + de_poetry_version_str(sanitize_version(dev)))

