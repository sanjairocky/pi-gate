from typing import Optional
import os
import yaml
import re


path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')


def path_constructor(loader, node):
    return os.path.expandvars(node.value)


class EnvVarLoader(yaml.SafeLoader):
    pass


EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
EnvVarLoader.add_constructor('!path', path_constructor)


def load_config():
    with open(os.getenv('CONFIG_FILE_LOCATION', 'config.yml'), "r") as stream:
        return yaml.load(stream, Loader=EnvVarLoader)


def get_value(keys: list, values: dict):
    key = keys.pop()
    if len(keys) == 0:
        return values[key]
    else:
        return get_value(keys, values=values[key])


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        try:
            keys = var_name.split('.')
            keys.reverse()
            return get_value(keys, load_config())
        except KeyError:
            return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)
