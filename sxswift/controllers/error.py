'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import bottle
from sxswift.hooks import RESPONSE_HOOKS


def default_error_handler(exc):
    # Bottle is not running after_request hooks
    # on errors.
    for response_hook in RESPONSE_HOOKS:
        response_hook()

    bottle.response.content_type = 'text/plain'

    if hasattr(exc, 'body'):
        return exc.body

    return ''
