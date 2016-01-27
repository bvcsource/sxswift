'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging
import logging.config

import colorama
colorama.init()

from sxswift.utils.string_helpers import is_truthy

logger = logging.getLogger(__name__)

# TODO: move these logging settings to conf
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            'format': (
                colorama.Style.RESET_ALL +
                '%(asctime)s ' +
                colorama.Fore.YELLOW + colorama.Style.BRIGHT +
                '[%(levelname)s]' +
                colorama.Fore.BLUE + ' %(name)s: ' +
                colorama.Style.RESET_ALL + colorama.Style.BRIGHT +
                '%(message)s' + colorama.Style.RESET_ALL
            )
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}


class RequestLoggingMiddleware(object):
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf

    def __call__(self, env, start_response):
        ip_address = env.get('REMOTE_ADDR')
        msg = [
            '[', ip_address, '] ',
            env['SERVER_PROTOCOL'], ' ', env['REQUEST_METHOD'],
            ' ', env['PATH_INFO'], '\n'
        ]
        for key, value in env.iteritems():
            if key.startswith('HTTP_'):
                msg.append(key[5:] + ': ' + value + '\n')
        msg.append('\n')

        if is_truthy(self.conf.get('log_response_status')):
            def start_wrapper(status, headers):
                msg.append(status)
                return start_response(status, headers)
        else:
            start_wrapper = start_response

        resp = self.app(env, start_wrapper)
        logger.info(''.join(str(piece) for piece in msg))
        return resp


def app_factory(global_config, **local_conf):
    conf = global_config.copy()
    conf.update(local_conf)

    logging.config.dictConfig(LOGGING)

    def filter_app(app):
        return RequestLoggingMiddleware(app, conf)
    return filter_app
