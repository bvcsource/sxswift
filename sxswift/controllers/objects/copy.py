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
from sxswift.lib.objects.copier import ObjectCopier
from sxswift.utils.string_helpers import is_truthy

logger = logging.getLogger(__name__)


def get_destination():
    dest = bottle.request.get_header('destination', None)
    if dest is None:
        raise bottle.HTTPError(400, 'No Destination header')

    dest = dest.strip().lstrip('/')
    dst_container, _, dst_object = dest.partition('/')
    if not dst_container or not dst_object:
        raise bottle.HTTPError(400, 'Incorrect Destination header')

    return dst_container, dst_object


@sxswift_route
@auth_name
@requires_priv('read-write')
def copy_object(api_ver, account, container, object):
    _validate_object(api_ver, account, container, object)

    fresh = bottle.request.get_header('x-fresh-metadata')
    fresh = is_truthy(fresh)

    dst_container, dst_object = get_destination()

    meta = {}
    for key, value in bottle.request.headers.iteritems():
        key = key.lower()
        if key.startswith('x-object-meta-'):
            meta[key] = value

    content_type = bottle.request.get_header('content-type')
    if content_type:
        meta['content-type'] = content_type

    copier = ObjectCopier(
        container, object,
        dst_container, dst_object
    )
    copier.copy(meta=meta, fresh_meta=fresh)

    bottle.response.set_header('x-timestamp', 0)
    bottle.response.status = 201
