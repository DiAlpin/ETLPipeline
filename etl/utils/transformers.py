import sys
import importlib.util


def py_files(path):
    python_files = [file for file in path.iterdir() if file.suffix == '.py' and file.is_file()]
    return python_files

def load_module(path):
    module_name = f'custom_tr_{path.stem}'
    spec = importlib.util.spec_from_file_location(module_name, path.as_posix())
    init_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = init_module
    spec.loader.exec_module(init_module)
    return module_name
