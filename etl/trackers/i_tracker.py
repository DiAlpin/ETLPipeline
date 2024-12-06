"""Tracker baseclass module"""

# Author: Daniel Broboana <daniel.broboana@gmail.com>

from abc import ABC, abstractmethod

from etl.datasets.metadata import Metadata


class ITracker(ABC):
    """
    Abstract base class for tracking performance and generating
    historical data.
    """

    @abstractmethod
    def gen_history(self):
        """
        Abstract method that generate historical tracking data.
        """

    def tracker_build_metadata(self):
        """
        Create metadata from performance logs and history.
        """
        traker_perf_log = getattr(self, 'traker_perf_log')
        return Metadata(traker_perf_log, self.gen_history())
