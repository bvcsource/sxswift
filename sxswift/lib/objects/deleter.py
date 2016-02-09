'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging

from sxclient.exceptions import SXClusterNotFound, SXClusterFatalError

from sxswift.lib.exceptions import NotFound, Conflict
from sxswift.lib.objects.common import ObjectProcessor
from sxswift.sx import get_sxcontroller

logger = logging.getLogger(__name__)


class ObjectDeleter(ObjectProcessor):
    def delete(self):
        sxcontroller = get_sxcontroller()
        if self.object_path.endswith('/'):
            try:
                file_objects = sxcontroller.listFiles.json_call(self.vol_name, recursive=True, filter=self.object_path)
            except SXClusterNotFound:
                raise NotFound
            except SXClusterFatalError:
                raise Conflict
            if(len(file_objects['fileList']) != 1):
                raise Conflict
            self.object_path += '.sxnewdir'
        try:
            sxcontroller.deleteFile.call(self.vol_name, self.object_path)
        except SXClusterNotFound:
            raise NotFound
        except SXClusterFatalError:
            # TODO: we should have better exception handling in sxclient
            raise Conflict
