'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import bottle

from sxswift.controllers.accounts.common import _validate_account
from sxswift.http_helpers.decorators import (
    sxswift_route,
    auth_name,
    requires_priv,
)
from sxswift.http_helpers.headers import get_meta_to_remove_and_update
from sxswift.lib.accounts import update_account_meta


@sxswift_route
@auth_name
@requires_priv('admin')
def post_account(api_ver, account):
    _validate_account(api_ver, account)
    remove_meta, update_meta = get_meta_to_remove_and_update(
        'x-account-meta-', 'x-remove-account-meta-'
    )
    update_account_meta(
        user_name=account, remove_list=remove_meta, update_dict=update_meta
    )
    bottle.response.status = 204
