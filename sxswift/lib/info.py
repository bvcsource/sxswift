'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging

import sxswift
from sxswift.lib.common import log_args
from sxswift.lib import constraints

logger = logging.getLogger(__name__)

INFO_DICT = None


def get_info_dict():
    global INFO_DICT

    if INFO_DICT is None:
        INFO_DICT = {
            "sxswift": {
                "version": sxswift.__version__
            }
        }
        for key in dir(constraints):
            if key != key.upper():
                continue
            value = getattr(constraints, key)
            if hasattr(value, 'pattern'):
                value = value.pattern
            elif isinstance(value, set):
                value = list(value)
            INFO_DICT[key.lower()] = value
    return INFO_DICT


@log_args(logger)
def get_info_data(is_admin=False):
    return get_info_dict()
