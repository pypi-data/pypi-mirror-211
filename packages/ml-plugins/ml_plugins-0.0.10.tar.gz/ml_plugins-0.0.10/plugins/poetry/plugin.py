import functools
from metaflow.includefile import IncludeFile 
from metaflow.exception import MetaflowException


def poetry():
    def decorator(function):
        @functools.wraps(function)
        def wrapper(self, *args):
            import subprocess
            import sys
            subprocess.run([sys.executable, '-m', 'poetry', 'install', '-C', self.path])
            return function(self, *args)
        return wrapper
    return decorator

