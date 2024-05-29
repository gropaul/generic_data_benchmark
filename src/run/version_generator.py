import os.path

from src.utils.names import get_dir_from_name
from src.run.search_space import Version
from src.utils.config import VERSIONS_DIR

build_benchmark_command = 'BUILD_BENCHMARK=1 GEN=ninja make '

def download_and_build_version(version: Version):

    # make dir for version if not exists
    version_name = get_dir_from_name(version['name'])
    version_dir = os.path.join(VERSIONS_DIR, version_name)

    if not os.path.exists(version_dir):
        os.makedirs(version_dir)

    github_commit_url = version['github_commit_url']
    splitted = github_commit_url.split('/commit/')
    repo = splitted[0] + '.git'
    commit = splitted[1]


    # if dir is empty, clone repo
    if not os.listdir(version_dir):
        clone_command = f'git clone {repo} "{version_dir}"'
        print(f'Cloning version {version_name}...')
        os.system(clone_command)
    else:
        print(f'Version {version_name} already exists, skipping cloning...')

    # checkout commit
    os.chdir(version_dir)

    checkout_command = f'git checkout {commit}'
    print(f'Checking out commit {commit}...')
    os.system(checkout_command)

    # build benchmark runner
    os.system(build_benchmark_command)



