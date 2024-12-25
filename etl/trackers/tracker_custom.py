import inspect
import networkx as nx
from etl.datasets.metadata import Metadata
from etl.trackers.i_tracker import ITracker
from etl.utils.trackers import (
    isolate_transformer_logic, 
    generate_nodes)


class CustomPDTransformerTraker(ITracker):
    def gen_history(self):
        method_txt = inspect.getsource(self.main_transformation)
        code_lines = isolate_transformer_logic(method_txt)
        nodes = generate_nodes(code_lines)

        his = nx.DiGraph()
        for n in nodes:
            his.add_node(n['node'], label=n['label'])
            for parent in n['parents']:
                his.add_edge(parent, n['node'])
        return his