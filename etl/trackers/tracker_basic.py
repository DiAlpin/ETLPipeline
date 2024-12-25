"""Basic Tracke module"""

# Author: Daniel Broboana <daniel.broboana@gmail.com>

from etl.trackers.i_tracker import ITracker



class BasicTracker(ITracker):
    """Tracker used by transformer that need only performance log."""

    def gen_history(self):
        """Generates None history for transformers that don't need history."""
        return None
