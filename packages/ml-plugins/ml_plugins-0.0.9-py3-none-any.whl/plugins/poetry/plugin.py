import functools
from metaflow.includefile import IncludeFile 
from metaflow.exception import MetaflowException


def poetry(path):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            import subprocess
            import sys
            subprocess.run([sys.executable, '-m', 'poetry', 'install', '-C', path])
            return function(*args, **kwargs)
        return wrapper
    return decorator
