'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

PRIVS_BY_NAME = {}


class Privilege(object):
    def __init__(self, name):
        self.name = name
        self.parents = []
        PRIVS_BY_NAME[name] = self

    def extends(self, priv):
        if self is priv:
            return True

        for parent in self.parents:
            if parent is priv or parent.extends(priv):
                return True
        return False

    def __str__(self):
        return '<%s: %s>' % (
            self.__class__.__name__,
            self.name
        )
    __repr__ = __str__


NO_PRIVS = Privilege('no-privs')
READ = Privilege('read')
READ.parents.append(NO_PRIVS)
READWRITE = Privilege('read-write')
READWRITE.parents.append(READ)
ADMIN = Privilege('admin')
ADMIN.parents.append(READWRITE)
