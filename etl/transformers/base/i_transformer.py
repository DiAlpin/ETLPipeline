from abc import ABC, abstractmethod


class ITransformer(ABC):

    @abstractmethod
    def main_transformation(self):
        """Here dshould define all the logic of the transformer"""
        pass
    