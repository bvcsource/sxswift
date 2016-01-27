'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import colorama
from decorator import decorator
colorama.init()

CALLED_MSG = colorama.Fore.WHITE + 'Function ' + \
    colorama.Fore.GREEN + '%s' \
    + colorama.Fore.WHITE + ' called with...\n' + \
    colorama.Fore.CYAN + 'ARGS: ' + colorama.Fore.WHITE + '%s\n' + \
    colorama.Fore.CYAN + 'KWARGS: ' + colorama.Fore.WHITE + '%s\n'

RESULT_MSG = colorama.Fore.WHITE + 'Function ' + \
    colorama.Fore.GREEN + '%s' \
    + colorama.Fore.WHITE + ' returned with...\n' + \
    colorama.Fore.CYAN + 'VALUE: ' + colorama.Fore.WHITE + '%s\n'


def log_args(logger):
    @decorator
    def wrapper(func, *args, **kwargs):
        fname = func.__name__
        logger.debug(CALLED_MSG, fname, args, kwargs)
        result = func(*args, **kwargs)
        logger.debug(RESULT_MSG, fname, result)
        return result
    return wrapper
