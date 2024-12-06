
import os

from pydantic import BaseModel
from pydantic import ValidationError



def singleton(cls):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def validate_config(
    base_model: BaseModel, 
    config: dict
    ):
    try:
        base_model(**config)  
    except ValidationError as e:
        raise ValueError(
            f'{"*"*30}\n' \
          +  'Invalid config for: ' \
          + f'{base_model.__class__.__name__}: ' \
          + f'\n{e.errors()}'
        )


def get_env_variable(name) -> dict|None:
    env_variable = os.environ.get(name)
    assert env_variable, f"Variable '{name}' is not defined as env variable!"
    return env_variable


# local functionality
def get_aws_credentials():
    keys = ['aws_access_key_id', 'aws_secret_access_key']
    return {k: get_env_variable(k) for k in keys}


def get_mysql_db_credentials(key):
    return get_env_variable(f'mysql_{key}')
