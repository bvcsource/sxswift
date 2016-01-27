'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from sxclient.exceptions import SXClusterNotFound, SXClusterFatalError

from sxswift.lib.exceptions import NotFound, Conflict
from sxswift.sx import get_sxcontroller
from sxswift.lib.meta import (
    get_meta_name,
    set_meta_name,
)


def get_metadata(vol, obj):
    sxcontroller = get_sxcontroller()
    try:
        resp = sxcontroller.getFileMeta.json_call(vol, obj)
    except SXClusterNotFound:
        raise NotFound
    except SXClusterFatalError:
        raise Conflict

    metas = {}
    for key, value in resp['fileMeta'].iteritems():
        key = str(get_meta_name(key))
        metas[key] = value.decode('hex')
    return metas


def encode_meta(meta):
    return {
        set_meta_name(key): value.encode('hex')
        for key, value in meta.iteritems()
    }


class ObjectProcessor(object):
    def __init__(self, user_name, vol_name, object_path):
        self.user_name = user_name
        self.vol_name = vol_name
        self.object_path = object_path

    def __repr__(self):
        return "[%s u:%s v:%s o:%s]" % (
            type(self).__name__, self.user_name, self.vol_name, self.object_path
        )
