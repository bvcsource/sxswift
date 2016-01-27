'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import bottle
from decorator import decorator

from sxswift.config import get_settings
from sxswift.lib.exceptions import SXSwiftException
from sxswift.privileges import PRIVS_BY_NAME, NO_PRIVS
from sxswift.utils.string_helpers import is_truthy


@decorator
def sxswift_route(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except SXSwiftException as exc:
        raise bottle.HTTPError(exc.status, exc.body)


@decorator
def auth_name(func, api_ver, account, *args, **kwargs):
    user = bottle.request.environ.get('sxswift.user')
    if user:
        account = user['name']
    return func(api_ver, account, *args, **kwargs)


def no_restrictions(fn):
    return fn


def requires_priv(priv_name):
    settings = get_settings()
    disable = settings.get('this.disable_access_restrictions')
    disable = is_truthy(disable)
    if disable:
        return no_restrictions

    if priv_name not in PRIVS_BY_NAME:
        raise Exception('Wrong access!')

    priv = PRIVS_BY_NAME[priv_name]

    @decorator
    def wrapper(func, *args, **kwargs):
        user = bottle.request.environ.get('sxswift.user')
        if not user:
            raise bottle.HTTPError(401)

        access = user.get('access', NO_PRIVS)
        if not access.extends(priv):
            raise bottle.HTTPError(403)
        return func(*args, **kwargs)
    return wrapper
