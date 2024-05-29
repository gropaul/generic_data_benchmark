from typing import TypedDict, List, Literal, Optional


class Version(TypedDict):
    name: str
    github_commit_url: str


Distribution = Literal['uniform', 'normal', 'exponential']
ValueType = Literal['random', 'sequential', 'constant']


class ValueSpace(TypedDict):
    type: ValueType
    offset: Optional[List[float]]  # percentage to the total row count
    avg_edges_per_node: Optional[List[int]]
    duplicates_distribution: Optional[List[Distribution]]


class Value(TypedDict):
    type: ValueType
    offset: float  # percentage to the total row count
    avg_edges_per_node: Optional[int]
    duplicates_distribution: Optional[Distribution]


class ColumnSpace(TypedDict):
    name: str
    value: ValueSpace


class Column(TypedDict):
    name: str
    value: Value


class TableSpace(TypedDict):
    name: str
    n_edges: List[int]

    columns: List[ColumnSpace]


class Table(TypedDict):
    name: str
    n_nodes: int
    n_edges: int

    columns: List[Column]


class SearchSpace(TypedDict):
    name: str
    query: str
    versions: List[Version]
    tables: List[TableSpace]


class SearchElement(TypedDict):
    name: str
    query: str
    tables: List[Table]
    version: Version
