'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import hashlib
import hmac
import time

import bottle

from sxswift.config import get_settings
from sxswift.utils.security import const_time_is_equal
from sxswift.lib.info import get_info_data
from sxswift.http_helpers.decorators import sxswift_route


ALLOWED_HMAC_METHODS = {
    'HEAD': ['HEAD', 'GET'],
    'GET': ['GET'],
}


def _get_hmac(method, path, expires, key):
    msg = '\n'.join([method, str(expires), path])
    digestmod = hashlib.sha1
    return hmac.new(key, msg=msg, digestmod=digestmod).hexdigest()


def _validate_signature(path, methods, sig, expires):
    try:
        expires = int(expires)
    except (ValueError, TypeError):
        raise bottle.HTTPError(400, 'expires not an integer')

    if expires < time.time():
        raise bottle.HTTPError(400, 'expires points at the time in past')

    has_valid_signature = False
    admin_key = get_settings().get('this.admin_key')
    for method in methods:
        digested_msg = _get_hmac(method, path, expires, admin_key)
        sigs_are_equal = const_time_is_equal(digested_msg, sig)
        has_valid_signature = has_valid_signature or sigs_are_equal
        # Even though we could break here we leave it as it is to
        # prevent timing attack even further.

    if not has_valid_signature:
        raise bottle.HTTPError(401, 'Incorrect sig for given expires')


@sxswift_route
def get_info():
    sig = bottle.request.params.get('swiftinfo_sig')
    expires = bottle.request.params.get('swiftinfo_expires')
    is_admin = sig or expires
    if is_admin:
        methods = ALLOWED_HMAC_METHODS[bottle.request.method]
        _validate_signature(bottle.request.path, methods, sig, expires)
    return get_info_data(is_admin=is_admin)
