"""Blender Tracke module"""

# Author: Daniel Broboana <daniel.broboana@gmail.com>

import networkx as nx

from etl.trackers.i_tracker import ITracker



class BlenderTraker(ITracker):
    def gen_history(self):
        his = nx.DiGraph()
        his.add_node(self._on_column, label=self._description)
        return his
