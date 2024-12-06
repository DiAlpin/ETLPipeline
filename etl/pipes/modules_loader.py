import os
import re
import sys
from pathlib import Path
import inspect
import importlib.util
from etl.utils.misc import singleton, validate_config
from etl.utils.transformers import py_files, load_module
from etl.transformers.base.i_transformer import ITransformer


@singleton
class CustomTransformersLoader:
    def __init__(self):
        print('Load custom transformer')
        self._project_dir = Path(os.environ.get('PIPELINEPATH')) / 'custom_transformers'
        self._valid_transformers = self._get_valid_transformers()
    
    def _iter_transformers(self):
        modules = []
        for path in py_files(self._project_dir):
            yield load_module(path)

    def _get_valid_transformers(self):
        classes = {}
        for name in self._iter_transformers():
            mod = sys.modules[name]
            for name, obj in inspect.getmembers(mod, inspect.isclass):
                if (
                    obj.__module__ == mod.__name__
                    and issubclass(obj, ITransformer)
                ): 
                    classes[obj.__name__] = mod.__name__
        return classes

    @property
    def current_transformers(self):
        return self._valid_transformers


@singleton
class DefaultComponentsLoader:
    def __init__(self):
        print('Load default components')
        self._load_component_module()

    def _load_component_module(self):
        from etl import extractors
        from etl import blenders
        from etl import transformers
        from etl import loaders



class InitComp:
    def __init__(self):
        self._default_comp = DefaultComponentsLoader()
        self._custom_comp = CustomTransformersLoader()
        self._modules = sys.modules

    def _get_common_class(self, comp, config):
        comp_name = config[f'{comp}_name']
        mod = self._modules[f'etl.{comp}s']
        
        # validate config using pydentic BaseModel
        base_model = getattr(mod, f'{comp_name}Model')
        validate_config(base_model, config)

        return getattr(mod, comp_name)(config)

    def extractor_class(self, config):
        return self._get_common_class('extractor', config)

    def blender_class(self, config):
        return self._get_common_class('blender', config)

    def transformer_class(self, config):
        tr_name = config['transformer_name']
        custom_tr = self._custom_comp.current_transformers

        if tr_name in custom_tr:
            module_name = custom_tr[tr_name]
            mod = self._modules[module_name]
            return getattr(mod, tr_name)(config)
        else:
            return self._get_common_class('transformer', config)

    def loader_class(self, config):
        return self._get_common_class('loader', config)


