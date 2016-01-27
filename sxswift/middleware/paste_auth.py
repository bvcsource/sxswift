'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import json
import Cookie

from sxswift.cache import get_cache
from sxswift.controllers.auth import AUTH_CACHE_TEMPLATE
from sxswift.privileges import PRIVS_BY_NAME, NO_PRIVS

KEYSTONE_HEADER = 'HTTP_X_IDENTITY_STATUS'
AUTH_COOKIE = 'sxsid'


class AuthMiddleware(object):
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf

    def load_user_data_from_keystone(self, env):
        token_auth = env.get('keystone.token_auth')
        if not token_auth:
            return None
        user = token_auth.user
        if not user:
            return None

        roles = env.get('HTTP_X_ROLES', '').split(',')

        access = PRIVS_BY_NAME['no-privs']
        if 'admin' in roles:
            access = PRIVS_BY_NAME['admin']

        user_data = {
            'meta': {
                'auth': 'keystone',
            },
            'name': env.get('HTTP_X_USER_NAME'),
            'access': access,
        }
        return user_data

    def _load_user_from_sxsid(self, sxsid, method):
        cache = get_cache()
        data = cache.get(AUTH_CACHE_TEMPLATE % sxsid)
        if not data:
            return None
        user_data = json.loads(data)
        if 'meta' not in user_data:
            user_data['meta'] = {}
        user_data['meta']['auth'] = method
        user_data['access'] = PRIVS_BY_NAME.get(user_data['access'], NO_PRIVS)
        return user_data

    def load_user_data_from_cookie(self, env):
        cookie_header = env.get('HTTP_COOKIE')
        if not cookie_header:
            return None

        cookies = Cookie.SimpleCookie()
        cookies.load(cookie_header)
        sxsid = cookies.get(AUTH_COOKIE)
        if not sxsid:
            return None
        return self._load_user_from_sxsid(sxsid.value, 'cookie')

    def load_user_data_from_url(self, env):
        parts = env['PATH_INFO'].split('/')
        sxsid = None
        for part in parts:
            if part.startswith('SXSID_'):
                sxsid = part[6:]
                break
        if not sxsid:
            return None
        return self._load_user_from_sxsid(sxsid, 'url')

    def __call__(self, env, start_response):
        user = None

        if env.get(KEYSTONE_HEADER, '').lower() == 'confirmed':
            user = self.load_user_data_from_keystone(env)

        if not user:
            user = self.load_user_data_from_cookie(env)

        if not user:
            user = self.load_user_data_from_url(env)

        env['sxswift.user'] = user
        return self.app(env, start_response)


def app_factory(global_config, **local_conf):
    conf = global_config.copy()
    conf.update(local_conf)

    def filter_app(app):
        return AuthMiddleware(app, conf)
    return filter_app
