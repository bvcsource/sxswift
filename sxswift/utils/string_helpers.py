'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

TRUE_VALUES = {True, 'true', '1', 'yes', 'on', 't', 'y'}


def is_truthy(value):
    if hasattr(value, 'lower'):
        value = value.lower()
    return value in TRUE_VALUES
