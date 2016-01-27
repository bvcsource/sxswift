'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import bottle
import logging

from sxswift.controllers.objects.common import _validate_object
from sxswift.http_helpers.decorators import (
    sxswift_route,
    auth_name,
    requires_priv,
)
from sxswift.lib.objects.loader import ObjectLoader, get_metadata

logger = logging.getLogger(__name__)


def get_range():
    range_h = bottle.request.get_header('range', None)
    if range_h is None:
        return None

    if range_h[:6].lower() != 'bytes=':
        raise bottle.HTTPError(400, 'Unsupported Range header')

    range_h = range_h.strip()[6:]
    range_h = range_h.split(',')
    tmp = []
    for piece in range_h:
        start, _, end = piece.partition('-')
        try:
            start = int(start)
        except (TypeError, ValueError):
            start = None

        try:
            end = int(end)
        except (TypeError, ValueError):
            end = None

        if start is None and end is None:
            continue

        tmp.append((start, end))

    if tmp:
        return tmp


@sxswift_route
@auth_name
@requires_priv('read')
def get_object(api_ver, account, container, object):
    # TODO: query params
    _validate_object(api_ver, account, container, object)
    object_loader = ObjectLoader(account, container, object)

    metadata = get_metadata(container, object)
    for key, value in metadata.iteritems():
        bottle.response.set_header(str(key), str(value))

    return object_loader.get_content_stream()
