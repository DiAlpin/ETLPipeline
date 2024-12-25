

import os
import re
from pathlib import Path
import inspect
import importlib.util
from etl.pipes.modules_loader import InitComp


class Pipe:
    def __init__(self, dataset):
        self._dataset = dataset
        self._comp_init = InitComp()
        self._transformers = []
        self._load = None

    @staticmethod
    def inject_extracted_dataset(config):
        extract = InitComp().extractor_class(config)
        dataset = extract()
        return Pipe(dataset)

    @staticmethod
    def inject_blended_dataset(datasets: list, config):
        blend = InitComp().blender_class(config)
        dataset = blend(datasets)
        return Pipe(dataset)

    def add_transformer(self, config):
        self._transformers.append(
            self._comp_init.transformer_class(config)
            )
        return self

    def set_loader(self, config):
        self._load = self._comp_init.loader_class(config)
        return self


    def run(self):
        for tr in self._transformers:
            try:
                self._dataset = tr(self._dataset)
            except Exception as e:
                raise ValueError(f'{tr.__class__.__name__}: {e}')

        if self._load :
            self._dataset = self._load(self._dataset)

        return self._dataset
