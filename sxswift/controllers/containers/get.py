'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging

import bottle

from sxswift.controllers.containers.common import _validate_container
from sxswift.controllers.containers.serializers import get_serializer
from sxswift.http_helpers.decorators import (
    sxswift_route,
    auth_name,
    requires_priv,
)
from sxswift.http_helpers.headers import get_format_from_request
from sxswift.lib.constraints import CONTAINER_LISTING_LIMIT
from sxswift.lib.containers import get_container_data

logger = logging.getLogger(__name__)


@sxswift_route
@auth_name
@requires_priv('read')
def get_container(api_ver, account, container):
    _validate_container(api_ver, account, container)

    prefix = bottle.request.params.get('prefix', '')
    delimiter = bottle.request.params.get('delimiter')
    limit = bottle.request.params.get('limit', '')
    marker = bottle.request.params.get('marker', '')
    end_marker = bottle.request.params.get('end_marker', '')
    path = bottle.request.params.get('path', '')

    if delimiter and (len(delimiter) > 1 or ord(delimiter) > 254):
        raise bottle.HTTPError(412, 'Bad delimiter')

    try:
        limit = int(limit)
    except ValueError:
        limit = CONTAINER_LISTING_LIMIT

    if limit > CONTAINER_LISTING_LIMIT:
        raise bottle.HTTPError(
            412, 'Maximum limit is %d' % CONTAINER_LISTING_LIMIT
        )

    if path:
        delimiter = '/'
        if path.endswith('/'):
            path = path[:-1]
        prefix = path

    container_data = get_container_data(
        user_name=account, vol_name=container, prefix=prefix,
        delimiter=delimiter, limit=limit, start_marker=marker,
        end_marker=end_marker
    )

    for key, value in container_data['meta'].iteritems():
        bottle.response.set_header(str(key), str(value))

    format_param = get_format_from_request()
    logger.debug('Accepted format: %s', format_param)

    serializer = get_serializer(format_param)
    bottle.response.content_type = serializer.content_type
    if not container_data['content']:
        bottle.response.status = 204

    return serializer.serialize(container_data)
