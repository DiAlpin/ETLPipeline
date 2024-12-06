import networkx as nx
from etl.datasets.metadata import Metadata
from etl.trackers.i_tracker import ITracker
from etl.trackers.tracker_custom import CustomPDTransformerTraker


def dummy_transformation(df):
    ### start
    df['A'] = df['B'] + df['C']
    ### end
    return df


class TestCustomPDTransformerTraker:
    traker_perf_log = [{
        'transformer': 'CustomPDTransformerTraker', 
        'exec_time': 0.1, 
        'memory_used': 1024
    }]

    # Create an CustomPDTransformerTraker instance 
    tracker = CustomPDTransformerTraker()

    # These attributes come from custom transformer class
    tracker.traker_perf_log = traker_perf_log
    tracker.main_transformation = dummy_transformation

    def test_gen_history_returns_digraph(self):
        """
        Test that gen_history() returns None for CustomPDTransformerTraker
        """
        history = self.tracker.gen_history()
        
        assert isinstance(history, nx.DiGraph), "Method should return a NetworkX DiGraph"
    
    def test_gen_history_graph_structure(self):
        """
        Test the specific structure of the generated graph
        """
        history = self.tracker.gen_history()

        assert len(history.nodes()) == 3, "Graph should have exactly 3 node"
        node = list(history.nodes(data=True))[0]
        assert node[0] == 'A', "Node should have A as its identifier"
        assert node[1]['label'] == 'df[B] + df[C]', "Node should have df[B] + df[C] as its label"
    

    def test_tracker_build_metadata(self):
        """
        Test the tracker_build_metadata method
        """
        metadata = self.tracker.tracker_build_metadata()
        
        assert isinstance(self.tracker, ITracker), "BasicTracker should be an instance of ITracker"
        assert isinstance(metadata, Metadata), "Should return a Metadata object"
        assert isinstance(metadata.col_history, nx.DiGraph), "History should be NetworkX DiGraph"
        assert metadata.perf_log == self.traker_perf_log, "Performance log should match"
    