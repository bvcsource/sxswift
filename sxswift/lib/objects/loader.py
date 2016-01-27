'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging
import signal

from sxclient import SXFileDownloader
from sxclient.exceptions import SXClusterNotFound, SXClusterFatalError

from sxswift.config import get_settings, register_signal
from sxswift.lib.exceptions import NotFound, Conflict
from sxswift.lib.common import log_args
from sxswift.lib.objects.common import (
    ObjectProcessor,

    # weird import issue, cannot import it directly in controllers/objects/get.py
    get_metadata,
)
from sxswift.sx import get_sxcontroller

logger = logging.getLogger(__name__)

_sxdownloader = None


def get_downloader():
    global _sxdownloader

    if _sxdownloader is None:
        sxcontroller = get_sxcontroller()
        settings = get_settings()

        kwargs = {}

        threads_no = settings.get('default.downloader.threads')
        if threads_no is not None:
            kwargs['threads_no'] = threads_no
            kwargs['number_of_connections'] = threads_no

        tmp_dir = settings.get('default.downloader.tmp_dir')
        if tmp_dir is not None:
            kwargs['tmp_dir'] = tmp_dir

        cache_files = settings.get('default.downloader.cache_files')
        if cache_files is not None:
            kwargs['cache_files'] = cache_files

        _sxdownloader = SXFileDownloader(sxcontroller, **kwargs)
        _sxdownloader.initialize()

    return _sxdownloader


# TODO: there should be a separate process that calls
# _sxdownloader.clean_cached_files() periodically.
# clean_cached_files method is safe.


def cleanup_downloader(sig):
    global _sxdownloader
    if _sxdownloader is None:
        return
    _sxdownloader.close()
    _sxdownloader = None


register_signal(signal.SIGINT, cleanup_downloader)
register_signal(signal.SIGTERM, cleanup_downloader)
register_signal(signal.SIGQUIT, cleanup_downloader)


class ObjectLoader(ObjectProcessor):

    @log_args(logger)
    def get_content_stream(self):
        try:
            downloader = get_downloader()
        except SXClusterNotFound:
            raise NotFound
        except SXClusterFatalError:
            raise Conflict

        return downloader.get_blocks_content_iterator(
            self.vol_name, self.object_path
        )
