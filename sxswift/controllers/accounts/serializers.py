'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import json

from lxml import etree


class JSONSerializer(object):
    content_type = 'application/json'

    def serialize(self, data):
        return json.dumps(data['content'])


class XMLSerializer(object):
    content_type = 'application/xml'
    KEYS = ('name', 'count', 'bytes')

    def serialize(self, data):
        root = etree.Element('account', name=data['name'])
        for dct in data['content']:
            el_container = etree.SubElement(root, 'container')
            for key in self.KEYS:
                el_name = etree.SubElement(el_container, key)
                el_name.text = str(dct[key])
        return etree.tostring(root, xml_declaration=True, encoding='utf-8')


class PlainSerializer(object):
    content_type = 'text/plain'

    def serialize(self, data):
        return '\n'.join(dct['name'] for dct in data['content']) + '\n'


def get_serializer(format):
    if format == 'application/json':
        return JSONSerializer()
    elif format.endswith('/xml'):
        return XMLSerializer()
    else:
        return PlainSerializer()
