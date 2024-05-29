from typing import List

from src.run.search_space import SearchSpace, ColumnSpace

UNIFORM_COLUMN_CONFIG: List[ColumnSpace] = [
    {
        'name': 'a',
        'value': {
            'offset': [0],
            'type': 'random',
            'avg_edges_per_node': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 32, 64, 128, 256, 512],
            'duplicates_distribution': ['uniform']
        }
    },
    {
        'name': 'b',
        'value': {
            'offset': [0],
            'type': 'random',
            'avg_edges_per_node': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 32, 64, 128, 256, 512],
            'duplicates_distribution': ['uniform']
        }
    }
]

SEARCH_SPACE: SearchSpace = {
    'name': 'Cyclic Join',
    'query': 'SELECT R1.a AS A, R2.a AS B, R3.a AS C FROM R R1 JOIN R R2 ON R1.b = R2.a JOIN R R3 ON R2.b = R3.a WHERE R3.b = R1.a;',
    'versions': [
        {
            'name': 'Baseline',
            'github_commit_url': 'https://github.com/gropaul/duckdb/commit/092bcff7b7ed7f116cc6102b1c196d2a10d6708a'
        },
        {
            'name': 'Chain Intersection (Hash Table)',
            'github_commit_url': 'https://github.com/gropaul/duckdb/commit/caf7c3e03134d6cd7c34fd95b377a7f230574655'
        },
    ],

    'tables': [
        {
            'name': 'R',
            'n_edges': [2_000_000],
            'columns': UNIFORM_COLUMN_CONFIG
        }
    ]
}
