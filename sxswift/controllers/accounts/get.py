'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging

import bottle

from sxswift.http_helpers.decorators import (
    sxswift_route,
    auth_name,
    requires_priv,
)
from sxswift.http_helpers.headers import get_format_from_request
from sxswift.lib.accounts import get_account_data
from sxswift.lib.constraints import ACCOUNT_LISTING_LIMIT
from sxswift.controllers.accounts.common import _validate_account
from sxswift.controllers.accounts.serializers import get_serializer

logger = logging.getLogger(__name__)


@sxswift_route
@auth_name
@requires_priv('read')
def get_account(api_ver, account):
    _validate_account(api_ver, account)

    prefix = bottle.request.params.get('prefix', '')
    delimiter = bottle.request.params.get('delimiter')
    limit = bottle.request.params.get('limit', '')
    marker = bottle.request.params.get('marker', '')
    end_marker = bottle.request.params.get('end_marker', '')

    if delimiter and (len(delimiter) > 1 or ord(delimiter) > 254):
        raise bottle.HTTPError(412, 'Bad delimiter')

    try:
        limit = int(limit)
    except ValueError:
        limit = ACCOUNT_LISTING_LIMIT

    if limit > ACCOUNT_LISTING_LIMIT:
        raise bottle.HTTPError(
            412, 'Maximum limit is %d' % ACCOUNT_LISTING_LIMIT
        )

    account_data = get_account_data(
        user_name=account, prefix=prefix, delimiter=delimiter,
        limit=limit, start_marker=marker, end_marker=end_marker
    )

    bottle.response.set_header('x-timestamp', account_data['timestamp'])
    for key, value in account_data['meta'].iteritems():
        bottle.response.set_header(str(key), str(value))

    format_param = get_format_from_request()
    logger.debug('Accepted format: %s', format_param)

    serializer = get_serializer(format_param)
    bottle.response.content_type = serializer.content_type
    if not account_data['content']:
        bottle.response.status = 204
        return ''

    return serializer.serialize(account_data)
