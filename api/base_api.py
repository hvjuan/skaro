"""Main base API.

Every new API endpoint should inherit this module. This encapsilates the
base headers as wells as allows the propagation of site wide policies.
"""

import cherrypy


class MethodNotAcceptedException(Exception):
    """Raised if an unknown method is requested."""


def handle_error():
    cherrypy.response.status = 500
    cherrypy.response.body = b'Check your parameters according to the docs.'


# @cherrypy.config(**{'request.error_response': handle_error})
class Api:
    """Base API class.

    Every class extending this object will need to implement
    the private methods."""

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, *args, **kwargs):
        """Base GET endpoint."""
        self._set_headers('GET')
        return self._get(*args, **kwargs)

    @cherrypy.tools.json_out()
    def POST(self, *args, **kwargs):
        """Base POST endpoint."""
        self._set_headers('POST')
        return self._post(*args, **kwargs)

    @cherrypy.tools.json_out()
    def PUT(self, *args, **kwargs):
        """Base PUT endpoint."""
        self._set_headers('POST')
        return self._put(*args, **kwargs)

    def _get(self, *args, **kwargs):
        raise NotImplementedError

    def _post(self, *args, **kwargs):
        raise NotImplementedError

    def _put(self, *args, **kwargs):
        raise NotImplementedError

    def _set_headers(self, method):
        """Sets base headers for backend endpoints.

        Easily enable headers to test Frontend instances without any
        cross-script chrome warnings.
        """
        if method not in frozenset({'GET', 'POST', 'PUT'}):
            raise MethodNotAcceptedException

        headers = cherrypy.response.headers
        headers['Access-Control-Allow-Origin'] = '*'
        headers['Access-Control-Allow-Credentials'] = 'true'
        headers['Access-Control-Allow-Methods'] = method
        headers['Access-Control-Allow-Headers'] = ('Origin, '
                                                   'Content-Type, Accept')
