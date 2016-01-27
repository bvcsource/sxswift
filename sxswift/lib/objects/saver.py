'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import hashlib
import logging

from sxclient import SXFileUploader

from sxswift.lib.common import log_args
from sxswift.lib.exceptions import UnprocessableEntity
from sxswift.lib.objects.common import ObjectProcessor
from sxswift.lib.meta import set_meta_name
from sxswift.sx import get_sxcontroller


logger = logging.getLogger(__name__)


class HashStream(object):
    def __init__(self, stream):
        self._stream = stream
        self._md5 = hashlib.md5()
        self._length = 0

    def read(self, chunk_size):
        chunk = self._stream.read(chunk_size)
        self._md5.update(chunk)
        self._length += len(chunk)
        return chunk

    def get_hash(self):
        return self._md5.hexdigest()

    def get_length(self):
        return self._length


class ObjectSaver(ObjectProcessor):

    META_KEYS = {'last-modified', 'content-type', 'content-length', 'etag'}

    def __init__(self, user_name, vol_name, object_path):
        super(ObjectSaver, self).__init__(user_name, vol_name, object_path)
        self.metadata = {}

    def _get_encoded_metadata(self):
        return {
            set_meta_name(key): str(value).encode('hex')
            for key, value in self.metadata.iteritems()
            if key in self.META_KEYS
        }

    def update_metadata(self, metadata):
        self.metadata.update(metadata)

    @log_args(logger)
    def upload_from_stream(self, stream):
        hash_stream = HashStream(stream)
        sxcontroller = get_sxcontroller()

        def before_flush(context):
            md5 = hash_stream.get_hash()
            etag = self.metadata['etag']
            if etag and etag != md5:
                raise UnprocessableEntity()

            self.metadata['etag'] = md5
            if 'content-length' not in self.metadata:
                content_length = hash_stream.get_length()
                self.metadata['content-length'] = content_length

            meta = self._get_encoded_metadata()
            sxcontroller.initializeAddChunk.call(
                context.token,
                context.uploaded_blocks,
                [],
                fileMeta=meta
            )

        file_uploader = SXFileUploader(sxcontroller)
        file_uploader.upload_stream(
            volume=self.vol_name,
            file_size=self.metadata['content-length'],
            file_name=self.object_path,
            stream=hash_stream,
            before_flush=before_flush,
        )
