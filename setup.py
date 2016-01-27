'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import os
import re

from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pip.req import parse_requirements

packages = ['sxswift']


def get_version():
    path = os.path.join('sxswift', '__init__.py')
    pattern = re.compile(r"^__version__ = '(?P<ver>\d+\.\d+\.\d+)'$")
    match = None
    with open(path, 'r', 'utf-8') as fo:
        for line in fo:
            match = pattern.match(line)
            if match:
                break

    if not match:
        raise AttributeError('No __version__ in __init__.py')

    return match.groupdict()['ver']


def get_requirements(path):
    try:
        from pip.download import PipSession
        parsed_file = parse_requirements(path, session=PipSession())
    except (ImportError, TypeError):
        parsed_file = parse_requirements(path)
    return [str(ir.req) for ir in parsed_file]


def get_description_from_file(path):
    with open(path, 'r', 'utf-8') as fo:
        readme = fo.read()
    return readme


setup(
    name='sxswift',
    version=get_version(),
    description='SXSwift - translate Swift protocol into SX',
    long_description=get_description_from_file('README.rst'),
    author='Skylable Ltd.',
    author_email='sx-users@lists.skylable.com',
    packages=packages,
    install_requires=get_requirements('requirements.txt'),
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
    entry_points='''
        [paste.app_factory]
        main=sxswift.core:app_factory

        [paste.filter_factory]
        auth=sxswift.middleware.paste_auth:app_factory
        logging=sxswift.middleware.paste_request_logging:app_factory
        cors=sxswift.middleware.paste_cors:app_factory
    '''
)
