'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging
import json
import random
import string
import sxclient

from sxswift.sx import get_sxcontroller
from sxswift.lib.common import log_args
from sxswift.lib.exceptions import NotFound
from sxswift.lib.meta import get_meta_name, set_meta_name

logger = logging.getLogger(__name__)


def get_user_object(name):
    if name is None:
        raise NotFound

    sxcontroller = get_sxcontroller()
    users = sxcontroller.listUsers.json_call()

    if name not in users:
        create_user(name)
        users = sxcontroller.listUsers.json_call()
        if name not in users:
            raise NotFound

    return users[name]


def get_user_meta(user):
    try:
        return {
            get_meta_name(key): value
            for key, value in json.loads(user['userDesc']).iteritems()
        }
    except Exception:
        return {}


def create_user(user_name):
    sxcontroller = get_sxcontroller()
    password = ''.join(random.choice(string.letters + string.digits) for i in range(16))
    new_user_data = sxclient.UserData.from_userpass_pair(user_name, password, sxcontroller.get_cluster_uuid())
    sxcontroller.createUser.json_call(userName=user_name, userType="normal", userKey=new_user_data.secret_key.encode('hex'))


def create_user_if_not_exists(user_name):
    try:
        get_user_object(user_name)
    except NotFound:
        pass
    create_user(user_name)


@log_args(logger)
def update_account_meta(user_name, remove_list, update_dict):
    user = get_user_object(user_name)
    meta = get_user_meta(user)
    for key in remove_list:
        meta.pop(key, None)

    meta.update(update_dict)
    meta = {
        set_meta_name(key): value
        for key, value in meta.iteritems()
    }
    get_sxcontroller().modifyUser.call(
        user_name, desc=json.dumps(meta)
    )


@log_args(logger)
def get_account_data(
    user_name, prefix, delimiter, limit, start_marker, end_marker
):
    # TODO: at the moment delimiter is ignored since I'm not 100% sure how
    # it works on swift's side
    sxcontroller = get_sxcontroller()
    user = get_user_object(user_name)
    user_meta = get_user_meta(user)

    result = {
        'name': user_name,
        'content': None,
        'timestamp': 0,  # not supported by sx
        'meta': {
            'x-timestamp': 0,
            'x-account-object-count': 0,
            'x-account-container-count': 0,
            'x-account-bytes-used': 0
        },
    }
    result['meta'].update(user_meta)

    content = []

    volumes = sxcontroller.listVolumes.json_call()
    for vol_name, vol_info in volumes['volumeList'].iteritems():
        owner = vol_info['owner']
        if owner != user_name:
            continue

        if start_marker and vol_name <= start_marker:
            continue

        if end_marker and vol_name > end_marker:
            continue

        if not vol_name.startswith(prefix):
            continue

        result['meta']['x-account-container-count'] += 1

        count = 0
        size = 0
        sxfiles = sxcontroller.listFiles.json_call(vol_name, recursive=True)
        for sxfile in sxfiles['fileList'].itervalues():
            count += 1
            result['meta']['x-account-object-count'] += 1
            file_size = sxfile['fileSize']
            size += file_size
            result['meta']['x-account-bytes-used'] += file_size

        content.append({
            'count': count,
            'bytes': size,
            'name': vol_name
        })

        if len(result) >= limit:
            break

    result['content'] = sorted(content, key=lambda el: el['name'])
    return result
