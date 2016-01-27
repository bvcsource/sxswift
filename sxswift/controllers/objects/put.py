'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from datetime import datetime

import bottle

from sxswift.controllers.objects.common import (
    _validate_object,
    get_content_type,
)
from sxswift.http_helpers.decorators import (
    sxswift_route,
    auth_name,
    requires_priv,
)
from sxswift.lib.constraints import MAX_FILE_SIZE
from sxswift.lib.objects.saver import ObjectSaver
from sxswift.utils.datetime_helpers import datetime_to_http_iso


def get_content_stream(metadata):
    # TODO: deal with chunked, i.e. parse chunks
    return bottle.request.body


def get_content_length():
    content_length = bottle.request.get_header('content-length', None)
    if content_length is not None:
        try:
            content_length = int(content_length)
        except ValueError:
            raise bottle.HTTPError(400, 'Incorrect Content-Length header')

        if content_length > MAX_FILE_SIZE:
            raise bottle.HTTPError(413, 'Your request is too large')

        return content_length

    transfer_encoding = bottle.request.get_header('transfer-encoding', None)
    if transfer_encoding != 'chunked':
        raise bottle.HTTPError(411, 'Mising content-Length header')

    return None


def get_copy_from(content_length):
    copy_from = bottle.request.get_header('x-copy-from', None)
    if copy_from and content_length:
        raise bottle.HTTPError(400, 'Copy requires a zero byte body')
    return copy_from


def get_etag():
    return bottle.request.get_header('etag', None)


@sxswift_route
@auth_name
@requires_priv('read-write')
def put_object(api_ver, account, container, object):
    _validate_object(api_ver, account, container, object)

    content_length = get_content_length()

    now = datetime.utcnow()

    params = {
        'last-modified': datetime_to_http_iso(now),
        'content-type': get_content_type(object),
        'content-length': content_length,
        'copy-from': get_copy_from(content_length),
        'etag': get_etag(),
    }

    content_stream = get_content_stream(params)

    object_saver = ObjectSaver(account, container, object)
    object_saver.update_metadata(params)
    object_saver.upload_from_stream(content_stream)

    bottle.response.status = 201
