'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import mimetypes

import bottle

from sxswift.lib.validators import object_name_is_valid
from sxswift.controllers.containers.common import _validate_container
from sxswift.utils.string_helpers import is_truthy


def _validate_object(api_ver, account, container, object):
    _validate_container(api_ver, account, container)

    if not object_name_is_valid(object):
        msg = 'Object name %s is invalid' % object
        raise bottle.HTTPError(400, msg)


def get_content_type(path):
    detect_content_type = bottle.request.get_header('x-detect-content-type')
    if is_truthy(detect_content_type):
        guessed_type, _ = mimetypes.guess_type(path)
        return guessed_type or 'application/octet-stream'

    content_type = bottle.request.get_header('content-type', None)
    if content_type is None:
        raise bottle.HTTPError(400, 'No content type')
    return content_type
