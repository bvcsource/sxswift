'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''


class SXSwiftException(Exception):
    status = 0

    def __init__(self, body=''):
        self.body = body
        super(SXSwiftException, self).__init__()


class NotFound(SXSwiftException):
    status = 404


class Conflict(SXSwiftException):
    status = 409


class UnprocessableEntity(SXSwiftException):
    status = 422
