'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import re

RE_ACCOUNT_NAME = re.compile(r'^((?!/).){0,256}$')
RE_CONTAINER_NAME = RE_ACCOUNT_NAME
RE_OBJECT_NAME = re.compile(r'^(.){0,1024}$')

ACCOUNT_LISTING_LIMIT = 10000
CONTAINER_LISTING_LIMIT = 10000

MAX_FILE_SIZE = 5368709122
VALID_API_VERSIONS = {'v1', 'v1.0'}
