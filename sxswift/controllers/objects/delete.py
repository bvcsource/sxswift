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
from sxswift.lib.objects.deleter import ObjectDeleter
from sxswift.lib.exceptions import NotFound


logger = logging.getLogger(__name__)


@sxswift_route
@auth_name
@requires_priv('read-write')
def delete_object(api_ver, account, container, object):
    _validate_object(api_ver, account, container, object)

    deleter = ObjectDeleter(account, container, object)
    try:
        deleter.delete()
    except NotFound:
        raise bottle.HTTPError(404, 'Object not found')

    bottle.response.set_header('x-timestamp', 0)
    bottle.response.status = 204
