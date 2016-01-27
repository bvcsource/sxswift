'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging
import signal

import requests

import sxclient
from sxswift import config


logger = logging.getLogger(__name__)
_sxcontroller = None


def configure_sx(application):
    settings = config.get_settings()
    logger.debug('Configure called with settings: %s.' % settings)

    # SX initialization
    global _sxcontroller
    user_data = sxclient.UserData.from_key_path(settings['sx.admin_key'])
    cluster = sxclient.Cluster(
        settings['sx.cluster_name'],
        ip_addresses=settings.get('sx.host_list'),
        is_secure=settings.get('sx.ssl', True),
        port=settings.get('sx.port'),
        verify_ssl_cert=settings.get('sx.verify_cert', True)
    )
    _sxcontroller = sxclient.SXController(cluster, user_data=user_data)
    logger.debug('SXController initialized.')

    # # SX cleanup initialization
    config.register_signal(signal.SIGINT, close_sxcontroller)
    config.register_signal(signal.SIGTERM, close_sxcontroller)
    config.register_signal(signal.SIGQUIT, close_sxcontroller)
    logger.debug('Cleanup actions initialized.')

    # Other stuff
    requests.packages.urllib3.disable_warnings()  # unnecessary noise

    logger.info('Fully configured SX.')


def get_sxcontroller():
    if _sxcontroller is None:
        raise TypeError('SXController not initialized')
    return _sxcontroller


def close_sxcontroller(sig):
    global _sxcontroller
    if _sxcontroller is None:
        return
    _sxcontroller.close()
    _sxcontroller = None
