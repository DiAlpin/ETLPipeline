import pytest
import networkx as nx
from dataclasses import dataclass
from etl.datasets.metadata import Metadata
from etl.trackers.i_tracker import ITracker
from etl.trackers.tracker_extractor import ExtractorTraker

# Mock classes to represent the context
@dataclass
class Table:
    column_names: list


class TestExtractorTraker:
    table = Table(column_names=['age', 'income', 'education'])
    data_source_label = 'test_source'
    traker_perf_log = [{
        'transformer': 'ExtractorTraker', 
        'exec_time': 0.1, 
        'memory_used': 1024
    }]

    # Create an ExtractorTraker instance
    tracker = ExtractorTraker()

    # These attributes come from extractor class
    tracker.data_source_label = data_source_label
    tracker.traker_perf_log = traker_perf_log

    def test_gen_history_returns_digraph(self):
        """
        Test that gen_history() returns a NetworkX DiGraph object
        """
        history = self.tracker.gen_history(self.table)

        assert isinstance(history, nx.DiGraph), "Method should return a NetworkX DiGraph"
    
    def test_gen_history_graph_structure(self):
        """
        Test the specific structure of the generated graph
        """
        history = self.tracker.gen_history(self.table)
        
        assert len(history.nodes()) == len(self.table.column_names), "Graph should have a node for each column"
        for node, data in history.nodes(data=True):
            assert node in self.table.column_names, f"Node {node} should be a column name"
            assert data['label'] == self.data_source_label, "All nodes should have the same label"
    
    
    def test_tracker_build_metadata(self):
        """
        Test the tracker_build_metadata method
        """
        metadata = self.tracker.tracker_build_metadata(self.table)
        
        assert isinstance(metadata, Metadata), "Should return a Metadata object"
        assert isinstance(metadata.col_history, nx.DiGraph), "Metadata history should be a DiGraph"
        assert len(metadata.col_history.nodes()) == len(self.table.column_names), "Metadata history should have nodes for each column"
        assert metadata.perf_log == self.traker_perf_log, "Performance log should match"