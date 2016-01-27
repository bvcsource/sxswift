'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import uuid
from datetime import datetime

import bottle

from sxswift.utils.datetime_helpers import datetime_to_http_iso


def set_common_headers():
    now = datetime.utcnow()
    bottle.response.set_header('date', datetime_to_http_iso(now))
    trans_id = bottle.request.get_header('x-trans-id')
    if not trans_id:
        trans_id = '5358-' + str(uuid.uuid4())  # 5358 = SX hex encoded
    bottle.response.set_header('x-trans-id', trans_id)


RESPONSE_HOOKS = [
    set_common_headers
]
REQUEST_HOOKS = []


def configure_hooks(application):
    for request_hook in REQUEST_HOOKS:
        application.add_hook('before_request', request_hook)
    for response_hook in RESPONSE_HOOKS:
        application.add_hook('after_request', response_hook)
