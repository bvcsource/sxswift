'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from sxswift.lib.objects.common import (
    ObjectProcessor,
    get_metadata,
    encode_meta,
)
from sxswift.sx import get_sxcontroller


class MetaSaver(ObjectProcessor):

    def save(self, new_meta):
        current_meta = get_metadata(self.vol_name, self.object_path)

        key = 'content-type'
        if key not in new_meta and key in current_meta:
            new_meta[key] = current_meta[key]

        sxcontroller = get_sxcontroller()
        file_info = sxcontroller.getFile.json_call(
            self.vol_name, self.object_path
        )

        blocks = [obj.keys()[0] for obj in file_info['fileData']]
        size = file_info['fileSize']

        # We create new file because this is the only way to alter
        # meta on sx file.
        resp = sxcontroller.initializeFile.call(
            self.vol_name, self.object_path, size, blocks,
            encode_meta(new_meta)
        )
        token = resp.json()['uploadToken']

        sxcontroller.flushUploadedFile.call_on_node(resp.node_address, token)
