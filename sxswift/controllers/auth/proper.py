'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import hashlib
import json
import os
import logging
import time

import bottle

from sxswift.cache import get_cache
from sxswift.config import get_users, get_settings
from sxswift.http_helpers.decorators import sxswift_route

AUTH_CACHE_TEMPLATE = 'sxsid:%s'


logger = logging.getLogger(__name__)

SECRET = 'c8SawvRkooa8HWhN'


@sxswift_route
def get_auth(path=None):
    user = bottle.request.get_header('x-auth-user', None)
    key = bottle.request.get_header('x-auth-key', None)
    if user is None or key is None:
        raise bottle.HTTPError(400)

    users = get_users()
    if user not in users:
	logger.debug("Unknown user '%s'" % user)
        raise bottle.HTTPError(401)

    user = users[user]
    if user['pwd'] != key:
	logger.debug("Wrong key for user '%s'" % user['name'])
        raise bottle.HTTPError(401)

    settings = get_settings()

    name = user['name']
    sxsid = hashlib.sha1(SECRET + name).hexdigest()
    sxsid += ':' + os.urandom(128).encode('hex')

    cache = get_cache()
    cache.set(AUTH_CACHE_TEMPLATE % sxsid, json.dumps(user))

    url = settings['this.storage_url'] + 'SXSID_' + sxsid
    ttl = settings['cache.expiration_time']
    exp = int(time.time()) + ttl
    bottle.response.set_cookie('sxsid', sxsid, max_age=ttl, expires=exp)
    bottle.response.set_header('x-storage-url', url)
    bottle.response.status = 200
