import json
import os
from typing import List, Dict, Any, Optional, Literal

import pandas as pd

from src.run.search_space import SearchElement
from src.utils.dicts import flatten_dict
from src.utils.names import get_search_space_results_dir, get_search_space_elements_dir


def get_median_runtime(runtimes: List[float]) -> float:
    runtimes = sorted(runtimes)
    length = len(runtimes)
    if length % 2 == 0:
        return (runtimes[length // 2 - 1] + runtimes[length // 2]) / 2
    else:
        return runtimes[length // 2]


def get_mean_runtime(runtimes: List[float]) -> float:
    return sum(runtimes) / len(runtimes)


Metric = Literal['median', 'mean']


def get_runtimes(search_space_name, metric: Metric = 'median') -> List[Optional[float]]:
    results_dir = get_search_space_results_dir(search_space_name)
    runtimes_collection = []
    files = os.listdir(results_dir)
    # sort the files by name
    files.sort(key=lambda x: int(x.split('.')[0]))
    for file in files:
        if file.endswith('.out'):
            with open(os.path.join(results_dir, file), 'r') as f:
                lines = f.readlines()

                if len(lines) == 0:
                    runtimes_collection.append(None)
                    print(f'Empty file: {file}')
                    continue
                has_error = False
                runtimes = []
                for line in lines:
                    try:
                        runtime = float(line)
                        runtimes.append(runtime)
                    except:
                        print(f'Error in file: {file}')
                        has_error = True
                        break

                if not has_error:
                    aggregate_runtime = get_median_runtime(runtimes) if metric == 'median' else get_mean_runtime(
                        runtimes)
                    runtimes_collection.append(aggregate_runtime)
                else:
                    runtimes_collection.append(None)

    return runtimes_collection


def get_configs(search_space_name: str) -> List[Dict[str, Any]]:
    elements_dir = get_search_space_elements_dir(search_space_name)
    configs = []
    files = os.listdir(elements_dir)
    # sort the files by name
    files.sort(key=lambda x: int(x.split('.')[0]))
    for file in files:
        if file.endswith('.json'):
            with open(os.path.join(elements_dir, file), 'r') as f:
                element: SearchElement = json.load(f)
                flattened_element = flatten_dict(element)
                configs.append(flattened_element)

    return configs


def load(search_space_name: str) -> pd.DataFrame:
    runtimes = get_runtimes(search_space_name)
    configs = get_configs(search_space_name)

    df = pd.DataFrame(configs)
    # save as csv with header
    df['runtime'] = runtimes
    return df
