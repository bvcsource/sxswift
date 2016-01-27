'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import bottle


FORMAT_ACCEPT_MAP = {
    'json': 'application/json',
    'xml': 'application/xml',
    'plain': 'text/plain',
}

SUPPORTED_FORMATS = {
    'application/json', 'application/xml', 'text/plain', 'text/xml'
}


def get_meta_to_remove_and_update(update_prefix, remove_prefix):
    update_meta = {}
    remove_meta = set()

    for key, value in bottle.request.headers.iteritems():
        key = key.lower()
        if key.startswith(update_prefix):
            value = value.strip()
            if value:
                update_meta[key] = value
            else:
                remove_meta.add(key)
        elif key.startswith(remove_prefix):
            meta_key = key.replace(remove_prefix, '', 1)
            meta_key = update_prefix + meta_key
            remove_meta.add(meta_key)

    return tuple(remove_meta), update_meta


def _get_format_from_accept_header():
    # see rfc2616 section 14.1
    format = bottle.request.get_header('Accept', '')
    format = format.split(',')
    format = (piece.strip().split(';') for piece in format)
    available_formats = []
    for piece in format:
        try:
            q = piece[1].split('=')[-1]
            q = float(q)
        except Exception:
            q = 0
        available_formats.append((q, piece[0]))
    available_formats = sorted(available_formats)

    for _, format in available_formats:
        ftype, _, fsubtype = format.partition('/')
        for supported_format in SUPPORTED_FORMATS:
            if supported_format.startswith(ftype):
                if fsubtype == '*':
                    return supported_format
                elif supported_format == format:
                    return supported_format
    return 'application/json'


def get_format_from_request():
    format_param = bottle.request.params.get('format')
    if not format_param:
        format_param = _get_format_from_accept_header()
    else:
        try:
            format_param = FORMAT_ACCEPT_MAP[format_param]
        except KeyError:
            raise bottle.HTTPError(406, 'format not supported')
    if format_param not in SUPPORTED_FORMATS:
        raise bottle.HTTPError(406, 'format not supported')
    return format_param
