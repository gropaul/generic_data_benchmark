from config.space import SEARCH_SPACE
from src.run.benchmark_runner import Runner
from src.run.data_generator import BenchmarkGenerator
from src.run.filter import filter_permutations, filter_all_duplicates_equal
from src.run.search_space_flattener import SPFlattener
from src.utils.time import seconds_to_time
from src.run.version_generator import download_and_build_version

if __name__ == '__main__':
    versions, flattened_search_space = SPFlattener.flatten_search_space(SEARCH_SPACE)
    # filtered_search_space = filter_permutations(flattened_search_space)

    filtered_search_space = filter_all_duplicates_equal(flattened_search_space)

    print(f'Search space has {len(flattened_search_space)} elements.')
    print(f'Filtered search space has {len(filtered_search_space)} elements.')

    time_seconds = len(filtered_search_space) * 3.6
    print(f'Estimated time to run data: {seconds_to_time(time_seconds)}')

    for version in versions:
        download_and_build_version(version)
        BenchmarkGenerator.get(filtered_search_space, version)

    Runner.run(filtered_search_space)
