'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import bottle

from sxswift.controllers.containers.common import _validate_container
from sxswift.http_helpers.decorators import (
    sxswift_route,
    auth_name,
    requires_priv,
)
from sxswift.lib.containers import delete_volume


@sxswift_route
@auth_name
@requires_priv('admin')
def delete_container(api_ver, account, container):
    _validate_container(api_ver, account, container)
    delete_volume(container)
    bottle.response.status = 204
