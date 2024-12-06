import pyarrow as pa
import networkx as nx
from etl.utils.metadata import append_to_graph, union_graphs


class Metadata:
    def __init__(
        self, 
        perf_log: list | None = None,
        col_history: nx.DiGraph | None = None
    ):
        self.perf_log = perf_log if perf_log else []
        self.col_history = col_history if col_history else nx.DiGraph()

    def __add__(self, other):
        if isinstance(other, Metadata):
            n_log = self.perf_log + other.perf_log
            n_his = append_to_graph(
                        base_graph=self.col_history, 
                        graph=other.col_history)            
            return Metadata(n_log, n_his)

        raise ValueError("Can only combine with another Metadata object")


def merge_metadatas(left_metadata, right_metadata):
    L = left_metadata.col_history.copy()
    R = right_metadata.col_history.copy()

    log = left_metadata.perf_log + right_metadata.perf_log

    U = union_graphs(L, R)    
    return Metadata(log, U)
