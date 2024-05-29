# filter permutations
from typing import List

from src.run.search_space import SearchElement, Value


def filter_all_duplicates_equal(elements: List[SearchElement]) -> List[SearchElement]:
    filtered_elements = []
    for element in elements:
        take = True
        for table in element['tables']:

            unique_duplicate = None

            for column in table['columns']:
                value: Value = column['value']
                if value['avg_edges_per_node'] is not None:
                    duplicates = value['avg_edges_per_node']
                    if unique_duplicate is None:
                        unique_duplicate = duplicates
                    else:
                        if unique_duplicate != duplicates:
                            take = False
                            break

            if not take:
                break
        if take:
            filtered_elements.append(element)
    return filtered_elements


def filter_permutations(elements: List[SearchElement]) -> List[SearchElement]:
    filtered_elements = []
    for element in elements:

        take = True

        min_size = None

        for table in element['tables']:

            table_size = table['rows']
            if min_size is None:
                min_size = table_size
            else:
                if table_size > min_size:
                    take = False
                    break
                else:
                    min_size = table_size

            min_duplicates = None

            for column in table['columns']:
                value: Value = column['value']
                if value['avg_edges_per_node'] is not None:
                    duplicates = value['avg_edges_per_node']
                    if min_duplicates is None:
                        min_duplicates = duplicates
                    else:
                        if duplicates > min_duplicates:
                            take = False
                            break
                        else:
                            min_duplicates = duplicates
        if take:
            filtered_elements.append(element)
    return filtered_elements
