"""Authentication utils."""

import cherrypy

import settings


def header_auth(f):
    """Simple endpoint header auth decorator.

    Raises:
        cherrypy.HTTPError: raises 401 if not authorized.
    """
    def process(*args, **kwargs):
        auth_code = cherrypy.request.headers.get('Authorization')
        if auth_code == settings.ACCESS_KEY:
            return f(*args, **kwargs)
        raise cherrypy.HTTPError(401, 'Unathorized')
    return process
