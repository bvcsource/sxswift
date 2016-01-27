'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from datetime import datetime

from sxswift.sx import get_sxcontroller
from sxswift.lib.objects.common import (
    get_metadata,
    encode_meta,
)
from sxswift.utils.datetime_helpers import datetime_to_http_iso


class ObjectCopier(object):
    def __init__(self, src_vol, src_path, dst_vol, dst_path):
        self.src_vol = src_vol
        self.src_path = src_path
        self.dst_vol = dst_vol
        self.dst_path = dst_path

    def copy(self, meta, fresh_meta):
        sxcontroller = get_sxcontroller()
        metadata = get_metadata(self.src_vol, self.src_path)

        clean_meta = {
            'etag': metadata.get('etag', ''),
            'content-type': metadata.get('content-type', 'application/octet-stream'),
            'last-modified': datetime_to_http_iso(datetime.utcnow()),
        }

        if not fresh_meta:
            for key, value in meta:
                clean_meta[key] = value
        meta = clean_meta

        file_info = sxcontroller.getFile.json_call(
            self.src_vol, self.src_path
        )

        blocks = [obj.keys()[0] for obj in file_info['fileData']]
        size = file_info['fileSize']

        resp = sxcontroller.initializeFile.call(
            self.dst_vol, self.dst_path, size, blocks,
            encode_meta(meta)
        )
        token = resp.json()['uploadToken']

        sxcontroller.flushUploadedFile.call_on_node(resp.node_address, token)
