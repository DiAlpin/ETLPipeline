import networkx as nx
from etl.trackers.i_tracker import ITracker
from etl.datasets.metadata import Metadata

class ExtractorTraker(ITracker):
    def gen_history(self, table):
        his = nx.DiGraph()
        for node in table.column_names:
            his.add_node(node, label=self.data_source_label)
        return his

    # TODO: not elegant to overwrite the method but kepp it for now
    def tracker_build_metadata(self, table):
        return Metadata(self.traker_perf_log, self.gen_history(table))
