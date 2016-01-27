'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from sxswift.http_helpers.decorators import sxswift_route
from sxswift.http_helpers.validators import validate_api_version
from sxswift.lib.endpoints import get_endpoints_info


@sxswift_route
def get_endpoints(api_ver, path=None):
    validate_api_version(api_ver)
    return get_endpoints_info()
