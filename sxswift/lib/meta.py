'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

META_PREFIX = 'sx-'


def get_meta_name(name):
    if name.startswith(META_PREFIX):
        return name[len(META_PREFIX):]
    return name


def set_meta_name(name):
    return META_PREFIX + name
