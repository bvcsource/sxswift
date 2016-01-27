'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import json
import time

import bottle

from sxswift.config import get_settings
from sxswift.controllers.containers.common import _validate_container
from sxswift.controllers.containers.post import post_container
from sxswift.http_helpers.decorators import (
    sxswift_route,
    auth_name,
    requires_priv,
)
from sxswift.lib.containers import create_volume_if_not_exists
from sxswift.lib.accounts import create_user_if_not_exists


@sxswift_route
@auth_name
@requires_priv('admin')
def put_container(api_ver, account, container):
    _validate_container(api_ver, account, container)
    settings = get_settings()
    size = bottle.request.get_header('x-container-meta-quota-bytes', '')
    try:
        size = int(size)
    except ValueError:
        size = settings['default.volume.size']

    info = {'created_by': 'sxswift', 'created_at': time.time()}
    info = json.dumps(info).encode('hex')

    create_user_if_not_exists(account)

    created = create_volume_if_not_exists(
        vol_name=container, user_name=account, size=size,
        replica_count=settings['default.volume.replica_count'],
        max_revisions=settings['default.volume.max_revisions'],
        meta={'creation_info': info}
    )
    bottle.response.status = 201 if created else 202
    post_container(api_ver, account, container)
