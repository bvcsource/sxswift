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
from sxswift.http_helpers.headers import get_meta_to_remove_and_update
from sxswift.lib.containers import update_container_meta


@sxswift_route
@auth_name
@requires_priv('admin')
def post_container(api_ver, account, container):
    _validate_container(api_ver, account, container)
    remove_meta, update_meta = get_meta_to_remove_and_update(
        'x-container-meta-', 'x-remove-container-meta-'
    )

    # TODO: add max volume size change

    # TODO: handle custom headers:
    # X-Container-Read, X-Container-Write, X-Versions-Location,
    # X-Remove-Versions-Location, X-Container-Meta-Web-Directory-Type

    size = bottle.request.get_header('x-container-meta-quota-bytes', '')
    try:
        size = int(size)
    except ValueError:
        size = None

    update_container_meta(
        user_name=account, vol_name=container, remove_list=remove_meta,
        update_dict=update_meta, new_size=size
    )
    bottle.response.status = 204
