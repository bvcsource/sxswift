'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging
import json
import collections
from datetime import datetime

from sxclient.exceptions import SXClusterNotFound, SXClusterFatalError

from sxswift.lib.accounts import get_user_object
from sxswift.lib.common import log_args
from sxswift.lib.exceptions import NotFound, Conflict
from sxswift.lib.meta import get_meta_name, set_meta_name
from sxswift.utils.datetime_helpers import datetime_to_http_iso
from sxswift.sx import get_sxcontroller

logger = logging.getLogger(__name__)


def delete_volume(vol_name):
    sxcontroller = get_sxcontroller()
    try:
        sxcontroller.deleteVolume.call(vol_name)
    except SXClusterNotFound:
        raise NotFound
    except SXClusterFatalError:
        # TODO: we should have better exception handling in sxclient
        raise Conflict


def create_volume_if_not_exists(
    vol_name, user_name, size, replica_count, max_revisions, meta
):
    try:
        get_volume_object(vol_name)
        return False
    except NotFound:
        pass

    sxcontroller = get_sxcontroller()
    sxcontroller.createVolume.call(
        vol_name, size, user_name, replica_count, max_revisions, meta
    )
    return True


def get_volume_object(name):
    sxcontroller = get_sxcontroller()
    try:
        volume = sxcontroller.locateVolume.json_call(
            name, includeCustomMeta=True
        )
    except SXClusterNotFound:
        raise NotFound

    return volume


def get_volume_meta(vol_name):
    volume = get_volume_object(vol_name)
    meta = {
        get_meta_name(key): value.decode('hex')
        for key, value in volume['customVolumeMeta'].iteritems()
    }
    meta.pop('__SXSWIFT__', None)
    return meta


def modify_volume(vol_name, meta, new_size):
    meta = {
        set_meta_name(key): value.encode('hex')
        for key, value in meta.iteritems()
    }
    meta['__SXSWIFT__'] = ''
    get_sxcontroller().modifyVolume.call(
        vol_name, customVolumeMeta=meta, size=new_size
    )


def list_files(vol_name, prefix, delimiter, start_marker, end_marker, limit):
    sxcontroller = get_sxcontroller()
    file_objects = sxcontroller.listFiles.call(
        vol_name, recursive=True, limit=str(limit)
    ).content
    file_objects = json.loads(file_objects, object_pairs_hook=collections.OrderedDict)
    for file_name, file_object in file_objects['fileList'].iteritems():
        file_name = file_name.lstrip('/')
        file_meta = sxcontroller.getFileMeta.json_call(vol_name, file_name)
        file_meta = file_meta.get('fileMeta', {})
        last_modified = datetime.fromtimestamp(file_object['createdAt'])
        last_modified = datetime_to_http_iso(last_modified)
        yield {
            'hash': file_meta.get('sx-etag', '').decode('hex'),
            'content_type': file_meta.get('sx-content-type', '').decode('hex'),
            'last_modified': last_modified,
            'bytes': file_object['fileSize'],
            'name': file_name
        }


@log_args(logger)
def get_container_data(
    user_name, vol_name, prefix, delimiter, limit, start_marker, end_marker
):
    get_user_object(user_name)
    volume_meta = get_volume_meta(vol_name)

    file_objects = list_files(
        vol_name, prefix, delimiter, start_marker, end_marker, limit
    )

    result = {
        'name': vol_name,
        'content': [],
        'meta': {
            'x-timestamp': 0,
            'x-container-object-count': 0,
            'x-container-bytes-used': 0
        },
    }
    result['meta'].update(volume_meta)

    for file_object in file_objects:
        if len(result['content']) >= limit:
            break
        name = file_object['name']
        if start_marker and name <= start_marker:
            continue

        if end_marker and name > end_marker:
            continue

        if not name.startswith(prefix):
            continue

        result['meta']['x-container-object-count'] += 1

        if delimiter:
            if prefix:
                name = name[len(prefix):]
            parts = name.split(delimiter)
            if len(parts) > 1:
                dirname = parts[0] + '/'
                if start_marker and prefix + dirname <= start_marker:
                    continue
                if dirname != prefix:
                    subdir = {'subdir': u'%s' % (prefix + dirname)}
                    if len(result['content']) > 0 and result['content'][-1] == subdir:
                        continue
                    result['content'].append(subdir)
                    continue

        if name.endswith('.sxnewdir'):
            continue

        result['meta']['x-container-bytes-used'] += file_object['bytes']
        result['content'].append(file_object)

    return result


@log_args(logger)
def update_container_meta(
    user_name, vol_name, remove_list, update_dict, new_size
):
    get_user_object(user_name)
    meta = get_volume_meta(vol_name)

    for key in remove_list:
        meta.pop(key, None)

    meta.update(update_dict)
    modify_volume(vol_name, meta, new_size)
