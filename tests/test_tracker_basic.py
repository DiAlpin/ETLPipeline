import networkx as nx
from etl.datasets.metadata import Metadata
from etl.trackers.i_tracker import ITracker
from etl.trackers.tracker_basic import BasicTracker



class TestBasicTracker:
    traker_perf_log = [{
        'transformer': 'BasicTracker', 
        'exec_time': 0.1, 
        'memory_used': 1024
    }]

    # Create an BasicTracker instance 
    tracker = BasicTracker()

    # These attributes come from transformer class
    tracker.traker_perf_log = traker_perf_log

    def test_gen_history_returns_none(self):
        """
        Test that gen_history() returns None for BasicTracker
        """
        history = self.tracker.gen_history()
        
        assert history is None, "Method should return None"
        
    def test_tracker_build_metadata_with_none_history(self):
        """
        Test the tracker_build_metadata method with None history
        """
        metadata = self.tracker.tracker_build_metadata()
        
        assert isinstance(self.tracker, ITracker), "BasicTracker should be an instance of ITracker"
        assert isinstance(metadata, Metadata), "Should return a Metadata object"
        assert isinstance(metadata.col_history, nx.DiGraph), "History should be NetworkX DiGraph"
        assert metadata.perf_log == self.traker_perf_log, "Performance log should match"
    