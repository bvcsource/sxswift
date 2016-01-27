'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging

from sxswift.lib.common import log_args

logger = logging.getLogger(__name__)


@log_args(logger)
def get_endpoints_info():
    # TODO: should it return my own address?
    return {
        "endpoints": [],
        "headers": {}
    }
