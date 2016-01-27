'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from sxswift.lib.constraints import (
    RE_ACCOUNT_NAME,
    RE_CONTAINER_NAME,
    RE_OBJECT_NAME,
    VALID_API_VERSIONS,
)


def api_version_is_valid(api_ver):
    return api_ver in VALID_API_VERSIONS


def account_name_is_valid(name):
    return RE_ACCOUNT_NAME.match(name)


def container_name_is_valid(name):
    return RE_CONTAINER_NAME.match(name)


def object_name_is_valid(name):
    return RE_OBJECT_NAME.match(name)
