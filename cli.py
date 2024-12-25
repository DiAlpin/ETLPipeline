import os
import shutil
from pathlib import Path

env_content = """
PIPELINEPATH={project_dir}

### AWS Variables ###
aws_secret_access_key=
aws_access_key_id=
aws_bucket=
"""

custom_transformer_contant = """
from etl import iTransformer

class TransformerX(iTransformer):
    '''Example Transformer'''
    pass
"""

init_contant = """
from transformer_x import TransformerX

__all__ = [
    "TransformerX"
]
"""

def _write_file(contant, path):
    with open(path.as_posix(), "w") as file:
        file.write(contant)


def create_project(project_name):
    project_dir = Path.cwd() / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    custom_tr_dir = project_dir / 'custom_transformers' 
    custom_tr_dir.mkdir(parents=True, exist_ok=True)

    sql_dir = project_dir / 'sql' 
    sql_dir.mkdir(parents=True, exist_ok=True)

    _write_file(env_content.format(project_dir=project_dir), project_dir / '.env')
    _write_file('', project_dir / 'pipeline.py')
    _write_file('', project_dir / 'pipeline_config.py')
    _write_file(init_contant, custom_tr_dir / '__init__.py')
    _write_file(custom_transformer_contant, custom_tr_dir / 'transformer_x.py')

    print(f'Project {project_name} created at: {project_dir.as_posix()}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('[INVALID ARG] usage: python cli.py <project_name>')
    else:
        create_project(sys.argv[1])