'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import bottle
import logging

from sxswift.controllers.objects.common import (
    _validate_object,
    get_content_type,
)
from sxswift.http_helpers.decorators import (
    sxswift_route,
    auth_name,
    requires_priv,
)
from sxswift.lib.objects.metasaver import MetaSaver

logger = logging.getLogger(__name__)


@sxswift_route
@auth_name
@requires_priv('read-write')
def post_object(api_ver, account, container, object):
    _validate_object(api_ver, account, container, object)

    meta = {}
    for key, value in bottle.request.headers.iteritems():
        key = key.lower()
        if key.startswith("x-object-meta-"):
            meta[key] = value

    try:
        meta['content-type'] = get_content_type(object)
    except bottle.HTTPError:
        pass

    meta_saver = MetaSaver(account, container, object)
    meta_saver.save(meta)

    bottle.response.set_header('x-timestamp', 0)
    bottle.response.status = 202
