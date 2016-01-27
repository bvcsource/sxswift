'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''


def datetime_to_http_iso(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S')
