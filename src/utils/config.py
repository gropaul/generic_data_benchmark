import os

# environment variable BENCHMARK_WORKSPACE_DIR or default value /Users/paul/workspace/Generic Data Benchmarker/workspace
WORKSPACE_DIR = os.getenv('BENCHMARK_WORKSPACE_DIR', '/Users/paul/workspace/generic_data_benchmark/workspace')

SEARCH_SPACES_DIR = os.path.join(WORKSPACE_DIR, 'search_spaces')
VERSIONS_DIR = os.path.join(WORKSPACE_DIR, 'versions')
ANALYSIS_RESULTS_DIR = os.path.join(WORKSPACE_DIR, 'analysis')
