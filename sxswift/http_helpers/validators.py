'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import bottle

from sxswift.lib.validators import api_version_is_valid


def validate_api_version(api_ver):
    if not api_version_is_valid(api_ver):
        raise bottle.HTTPError(400, 'Incorrect api version')
