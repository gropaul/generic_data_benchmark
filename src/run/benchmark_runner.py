import os
import subprocess
from typing import List
from tqdm import tqdm

import shutil
from src.utils.names import get_dir_from_name
from src.run.search_space import SearchElement, Version
from src.utils.config import VERSIONS_DIR, SEARCH_SPACES_DIR


def get_run_command(version: Version, element: SearchElement, element_index: int) -> str:
    runner_repo_path = 'build/release/benchmark/benchmark_runner'
    version_name = get_dir_from_name(version['name'])
    runner_path = os.path.join(VERSIONS_DIR, version_name, runner_repo_path)

    search_space_name = get_dir_from_name(element['name'])
    benchmark_path = os.path.join('benchmark', search_space_name, f'{element_index}.benchmark')

    results_dir = os.path.join(SEARCH_SPACES_DIR, search_space_name, 'results')
    out_path = os.path.join(results_dir, f'{element_index}.out')

    runner_command = f'{runner_path} {benchmark_path} --threads=1 --out={out_path}'
    return runner_command


class Runner:
    @staticmethod
    def run(elements: List[SearchElement]):

        element = elements[0]
        search_space_name = get_dir_from_name(element['name'])
        results_dir = os.path.join(SEARCH_SPACES_DIR, search_space_name, 'results')
        if os.path.exists(results_dir):
            shutil.rmtree(results_dir)

        os.makedirs(results_dir)

        distinct_version_names = list()
        for element in elements:
            version_name = element['version']['name']
            if version_name not in distinct_version_names:
                distinct_version_names.append(version_name)

        print(f'Distinct version names: {distinct_version_names}')

        print(f'\nRunning {len(elements)} benchmarks... ')
        for (element_index, element) in enumerate(tqdm(elements)):
            version = element['version']
            run_command = get_run_command(version, element, element_index)
            print(run_command)
            os.system(run_command)
