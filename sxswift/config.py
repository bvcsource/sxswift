'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import importlib
import logging
import os
import signal

from sxswift.utils.string_helpers import is_truthy

logger = logging.getLogger(__name__)

_SETTINGS = None
_USERS = None


KEYS_INT = (
    'cache.expiration_time', 'sx.port',
    'default.volume.size', 'default.volume.replica_count',
    'default.volume.max_revisions', 'default.downloader.threads',
)
KEYS_BOOL = (
    'sx.verify_cert', 'sx.ssl', 'default.downloader.cache_files',
)
KEYS_COMMA_SEPARATED = ('sx.host_list', )


def preprocess_settings():
    for key in KEYS_INT:
        if key in _SETTINGS:
            _SETTINGS[key] = int(_SETTINGS[key])

    for key in KEYS_BOOL:
        if key in _SETTINGS:
            _SETTINGS[key] = is_truthy(_SETTINGS[key])

    for key in KEYS_COMMA_SEPARATED:
        if key in _SETTINGS:
            _SETTINGS[key] = [
                part.strip() for part in _SETTINGS[key].split(',')
            ]


def get_settings():
    global _SETTINGS
    if _SETTINGS is None:
        path = os.environ.get('SXSWIFT_SETTINGS')
        if not path:
            raise RuntimeError('SXSWIFT_SETTINGS env var not specified')
        else:
            module_path, _, obj_name = path.partition(':')
            _SETTINGS = importlib.import_module(module_path)
            if obj_name:
                _SETTINGS = getattr(_SETTINGS, obj_name)
    return _SETTINGS


def get_users():
    global _USERS
    if _USERS is None:
        _USERS = {}
        settings = get_settings()
        for key, value in settings.iteritems():
            if key.startswith('users.'):
                name = key[6:]
                _USERS[name] = {}
                value = value.split()
                _USERS[name]['name'] = name
                _USERS[name]['pwd'] = value[0]
                _USERS[name]['access'] = value[1]
    return _USERS


_SIGNALS = {}


def register_signal(sig, fn):
    if sig not in _SIGNALS:
        finalizers = []
        _SIGNALS[sig] = finalizers

        def handler(_sig, _frame):
            for finalizer in finalizers:
                finalizer(_sig)

        signal.signal(sig, handler)

    _SIGNALS[sig].append(fn)
