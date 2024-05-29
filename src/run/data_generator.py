import json
import os
from typing import List
import shutil

from src.utils.names import get_dir_from_name
from src.run.search_space import Table, Value, SearchElement, Version

from src.utils.config import SEARCH_SPACES_DIR, VERSIONS_DIR


class BenchmarkGenerator:
    @staticmethod
    def get(elements: List[SearchElement], version: Version):
        benchmark_scripts = []
        first_element = elements[0]
        for element in elements:
            benchmark_script = BenchmarkGenerator.get_benchmark_script(element)
            benchmark_scripts.append(benchmark_script)

        version_name = get_dir_from_name(version['name'])
        search_space_name = get_dir_from_name(first_element['name'])
        benchmark_dir = os.path.join(VERSIONS_DIR, version_name, 'benchmark', search_space_name)
        element_dir = os.path.join(SEARCH_SPACES_DIR, search_space_name, 'elements')

        # remove old benchmarks, even if they are not empty
        if os.path.exists(benchmark_dir):
            shutil.rmtree(benchmark_dir)

        if os.path.exists(element_dir):
            shutil.rmtree(element_dir)

        os.makedirs(benchmark_dir)
        os.makedirs(element_dir)

        for i, benchmark_script in enumerate(benchmark_scripts):
            benchmark_file = os.path.join(benchmark_dir, f'{i}.benchmark')
            element_file = os.path.join(element_dir, f'{i}.json')
            with open(benchmark_file, 'w') as f:
                f.write(benchmark_script)
            with open(element_file, 'w') as f:
                element_as_json = elements[i]
                json.dump(element_as_json, f)

    @staticmethod
    def get_benchmark_script(search_element: SearchElement) -> str:

        benchmark_script = 'load\n'

        seed_command = "SELECT setseed(0.412);"
        benchmark_script += seed_command + '\n'

        for table in search_element['tables']:
            table_statement = BenchmarkGenerator.get_create_table(table)
            benchmark_script += table_statement + '\n'

        benchmark_script += '\n'
        benchmark_script += 'run\n'
        benchmark_script += search_element['query']
        return benchmark_script

    @staticmethod
    def get_create_table(table: Table) -> str:
        table_name = table['name']
        rows = table['n_edges']

        columns_strings = []
        for column in table['columns']:
            column_name = column['name']
            column_value: Value = column['value']
            column_type = column_value['type']
            column_offset = column_value['offset']

            if column_type == 'random':
                column_duplicates = column_value['avg_edges_per_node']
                column_duplicates_distribution = column_value['duplicates_distribution']
                column_range = rows // column_duplicates
                column_string = f'CAST({column_offset} + round(random() * {column_range}) as BIGINT) as {column_name}'
                columns_strings.append(column_string)

            elif column_type == 'sequential':
                column_offset = column_value['offset']
                column_string = f'CAST({column_offset} + i as BIGINT) as {column_name}'
                columns_strings.append(column_string)

            elif column_type == 'constant':
                column_offset = column_value['offset']
                column_string = f'CAST({column_offset} as BIGINT) as {column_name}'
                columns_strings.append(column_string)

        columns_string = ', '.join(columns_strings)
        statement = f'CREATE TABLE {table_name} AS SELECT {columns_string} from range (0,{rows}) t(i);'
        return statement
