'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''


class CorsMiddleware(object):
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf
        allow_origins = conf.get('allow_origins', '').split(';')
        self.allow_origins = set(piece.strip() for piece in allow_origins)

        allow_methods = conf.get('allow_methods', '').split(';')
        self.allow_methods = set(piece.strip() for piece in allow_methods)

    def __call__(self, env, start_response):
        # This follows CORS specification. If Origin is in
        # allow origins it adds the Access-Control-* headers.
        # Also if method is OPTIONS then it does not process
        # the request anymore, just returns headers.
        origin = env.get('HTTP_ORIGIN')

        headers = []
        if '*' in self.allow_origins:
            headers.append(('Access-Control-Allow-Origin', '*'))
        elif origin in self.allow_origins:
            headers.append(('Access-Control-Allow-Origin', origin))

        if self.allow_methods:
            methods = ','.join(self.allow_methods)
            headers.append(('Access-Control-Allow-Methods', methods))
            headers.append(('Allow', methods))

        if env['REQUEST_METHOD'].upper() == 'OPTIONS':
            start_response('204 No Content', headers)
            return []

        def wrapper(status, inner_headers):
            for header in headers:
                inner_headers.append(header)
            return start_response(status, inner_headers)

        return self.app(env, wrapper)


def app_factory(global_config, **local_conf):
    conf = global_config.copy()
    conf.update(local_conf)

    def filter_app(app):
        return CorsMiddleware(app, conf)
    return filter_app
