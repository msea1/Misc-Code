import subprocess
from os import system

GEMINI_PROJECT_ID = 94

# grab commits to master branch

# https://docs.gitlab.com/ee/api/commits.html#list-repository-commits
# curl --header "PRIVATE-TOKEN: <your_access_token>" "https://gitlab.example.com/api/v4/projects/5/repository/commits"

# curl --header "PRIVATE-TOKEN: <your_access_token>" "https://git.spaceflight.com/api/v4/projects/94/repository/commits/"

# have to figure out SSL cert


# alternate, use local git
AUTHOR = "Matthew Carruth"

CD_GEMINI_CMD = "cd ~/Code/gemini/"
FETCH_CMD = f"git fetch -p"
LOG_CMD = f"git --no-pager log origin/master --author='{AUTHOR}' --pretty='format:%s' --after=2020-06-01 --before=2020-06-10"

subprocess.call(f"{CD_GEMINI_CMD} && {FETCH_CMD}", shell=True)
result = subprocess.call(f"{CD_GEMINI_CMD} && {LOG_CMD}", shell=True)
print(result)
