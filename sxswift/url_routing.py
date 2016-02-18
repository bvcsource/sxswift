'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

import logging

from sxswift.config import get_settings

logger = logging.getLogger(__name__)


def configure_urls(application):
    settings = get_settings()

    from sxswift.controllers.error import default_error_handler
    application.default_error_handler = default_error_handler


    from sxswift.controllers.auth import get_auth
    application.route(settings['auth.prefix'], 'GET', get_auth)


    from sxswift.controllers.home import get_home
    application.route('/', 'GET', get_home)


    from sxswift.controllers.healthcheck import get_healthcheck
    application.route('/healthcheck', 'GET', get_healthcheck)
    application.route('/healthcheck/', 'GET', get_healthcheck)


    from sxswift.controllers.info import get_info
    application.route('/info', 'GET', get_info)
    application.route('/info/', 'GET', get_info)


    from sxswift.controllers.endpoints import get_endpoints
    application.route('/<api_ver>/endpoints', 'GET', get_endpoints)
    application.route('/<api_ver>/endpoints/', 'GET', get_endpoints)


    from sxswift.controllers.accounts import (
        get_account,
        post_account,
    )
    application.route('/<api_ver>/<account>', 'GET', get_account)
    application.route('/<api_ver>/<account>', 'POST', post_account)


    from sxswift.controllers.containers import (
        get_container,
        put_container,
        post_container,
        delete_container,
    )
    application.route(
        '/<api_ver>/<account>/<container>',
        'GET',
        get_container
    )
    application.route(
        '/<api_ver>/<account>/<container>',
        'POST',
        post_container
    )
    application.route(
        '/<api_ver>/<account>/<container>',
        'PUT',
        put_container
    )
    application.route(
        '/<api_ver>/<account>/<container>',
        'DELETE',
        delete_container
    )


    from sxswift.controllers.objects import (
        get_object,
        put_object,
        post_object,
        copy_object,
        delete_object,
    )
    application.route(
        '/<api_ver>/<account>/<container>/<object:re:.+>',
        'GET',
        get_object
    )
    application.route(
        '/<api_ver>/<account>/<container>/<object:re:.+>',
        'PUT',
        put_object
    )
    application.route(
        '/<api_ver>/<account>/<container>/<object:re:.+>',
        'POST',
        post_object
    )
    application.route(
        '/<api_ver>/<account>/<container>/<object:re:.+>',
        'COPY',
        copy_object
    )
    application.route(
        '/<api_ver>/<account>/<container>/<object:re:.+>',
        'DELETE',
        delete_object
    )

    logger.info('Configured routing.')
