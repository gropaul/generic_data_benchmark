import itertools
from typing import List, Tuple

from src.run.search_space import SearchSpace, SearchElement, ColumnSpace, Column, Table, TableSpace, ValueSpace, Value, \
    Version


class SPFlattener:
    @staticmethod
    def flatten_value_space(value_space: ValueSpace) -> List[Value]:
        values: List[Value] = []
        if value_space['type'] == 'random':
            for avg_edges_per_node in value_space['avg_edges_per_node']:
                for duplicates_distribution in value_space['duplicates_distribution']:
                    for offset in value_space['offset']:
                        value: Value = {
                            'type': value_space['type'],
                            'offset': offset,
                            'avg_edges_per_node': avg_edges_per_node,
                            'duplicates_distribution': duplicates_distribution
                        }
                        values.append(value)
        elif value_space['type'] == 'sequential':
            for offset in value_space['offset']:
                value: Value = {
                    'type': value_space['type'],
                    'offset': offset,
                    'avg_edges_per_node': None,
                    'duplicates_distribution': None
                }
                values.append(value)
        elif value_space['type'] == 'constant':
            value: Value = {
                'type': value_space['type'],
                'offset': value_space['offset'][0],
                'avg_edges_per_node': None,
                'duplicates_distribution': None
            }
            values.append(value)

        return values

    @staticmethod
    def flatten_column_space(column_space: ColumnSpace) -> List[Column]:
        columns: List[Column] = []
        values = SPFlattener.flatten_value_space(column_space['value'])
        for value in values:
            column: Column = {
                'name': column_space['name'],
                'value': value
            }
            columns.append(column)
        return columns

    @staticmethod
    def flatten_table_space(table_space: TableSpace) -> List[Table]:
        tables: List[Table] = []
        for rows in table_space['n_edges']:
            columns_space = table_space['columns']
            columns_space_elements = [SPFlattener.flatten_column_space(column_space) for column_space in columns_space]

            # Calculate the Cartesian product of the three lists
            cross_product = list(itertools.product(*columns_space_elements))
            for product in cross_product:
                table: Table = {
                    'name': table_space['name'],
                    'n_edges': rows,
                    'columns': list(product)
                }
                tables.append(table)

        return tables

    @staticmethod
    def flatten_search_space(search_space: SearchSpace) -> Tuple[List[Version], List[SearchElement]]:
        elements: List[SearchElement] = []

        table_space = search_space['tables']
        table_space_elements = [SPFlattener.flatten_table_space(table_space) for table_space in table_space]
        cross_product = list(itertools.product(*table_space_elements))

        for version in search_space['versions']:
            for product in cross_product:
                element: SearchElement = {
                    'tables': list(product),
                    'name': search_space['name'],
                    'query': search_space['query'],
                    'version': version
                }
                elements.append(element)

        return search_space['versions'], elements
