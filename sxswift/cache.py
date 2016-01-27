'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from sxswift.config import get_settings
from dogpile.cache import make_region

import os

region = None


def get_cache():
    global region
    if region is None:
        settings = get_settings()
        region = make_region().configure_from_config(settings, 'cache.')
	if settings['cache.backend'] == 'dogpile.cache.dbm':
	    os.chmod(settings['cache.arguments.filename'], 0700)

    return region
