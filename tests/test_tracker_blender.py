import networkx as nx
from etl.datasets.metadata import Metadata
from etl.trackers.i_tracker import ITracker
from etl.trackers.tracker_blender import BlenderTraker



class TestBlenderTraker:
    on_column = 'test_column'
    description = 'Test Description'
    traker_perf_log = [{
        'transformer': 'BlenderTraker', 
        'exec_time': 0.1, 
        'memory_used': 1024
    }]

    # Create an BlenderTraker instance 
    tracker = BlenderTraker()

    # These attributes come from blendor class
    tracker._on_column = on_column
    tracker._description = description
    tracker.traker_perf_log = traker_perf_log

    def test_gen_history_returns_digraph(self):
        """
        Test that gen_history() returns a NetworkX DiGraph object
        """
        # Call the method
        history = self.tracker.gen_history()

        assert isinstance(history, nx.DiGraph), "Method should return a NetworkX DiGraph"

    def test_gen_history_graph_structure(self):
        """
        Test the specific structure of the generated graph
        """
        history = self.tracker.gen_history()

        assert len(history.nodes()) == 1, "Graph should have exactly one node"
        node = list(history.nodes(data=True))[0]
        assert node[0] == self.on_column, "Node should have the column name as its identifier"
        assert node[1]['label'] == self.description, "Node should have the description as its label"
    

    def test_tracker_build_metadata_with_history(self):
        """
        Test the tracker_build_metadata method with None history
        """
        metadata = self.tracker.tracker_build_metadata()

        assert isinstance(self.tracker, ITracker), "BlenderTraker should be an instance of ITracker"
        assert isinstance(metadata, Metadata), "Should return a Metadata object"
        assert isinstance(metadata.col_history, nx.DiGraph), "Method should return a NetworkX DiGraph"
        assert metadata.perf_log == self.traker_perf_log, "Performance log should match"
