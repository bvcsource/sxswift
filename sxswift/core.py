'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging

import bottle

from sxswift import config
from sxswift.url_routing import configure_urls
from sxswift.sx import configure_sx
from sxswift.hooks import configure_hooks
from sxswift.cache import get_cache

logger = logging.getLogger(__name__)


def app_factory(global_config, **local_conf):
    conf = global_config.copy()
    conf.update(local_conf)
    config._SETTINGS = conf
    config.preprocess_settings()

    application = bottle.Bottle()

    configure_sx(application)
    configure_urls(application)
    configure_hooks(application)
    get_cache()

    return application
