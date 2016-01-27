'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import bottle

from sxswift.http_helpers.decorators import sxswift_route


@sxswift_route
def get_home():
    bottle.response.status = 200
    bottle.response.content_type = 'text/plain'
    return 'SX-SWIFT'
