import inspect
import logging
import sys
import log.config.client_log_config
import log.config.server_log_config
from functools import wraps

if sys.argv[0].count('client'):
    # if 'client' has been found in sys.argv[0]
    # but it isn't 100%. It could be part of folder name or else.
    logger = logging.getLogger('app.client')
else:
    logger = logging.getLogger('app.server')

class Log():
    '''Fabric for decorators to logging'''
    def __init__(self):
        pass

    def __call__(self, func):
        '''Decorator for logging'''
        @wraps(func)
        def wrapper(*args, **kwargs):
            '''Decorated function'''
            res = func(*args, **kwargs)
            logger.debug(f'Function {func.__name__} was called from function {inspect.stack()[1].function}', stacklevel=2)
            return res
        return wrapper

def log_dec(func):
    '''Decorator for logging'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        '''Decorated function'''
        res = func(*args, **kwargs)
        logger.debug(f'Function {func.__name__} was called from function {inspect.stack()[1].function}', stacklevel=2)
        return res
    return wrapper