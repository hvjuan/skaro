"""URL API."""

import cherrypy

from api import base_api
from db import log as log_db
from db import url as url_db
from utils import auth


class Stats(base_api.Api):

    exposed = True

    @auth.header_auth
    def _get(self, short_url):
        """Gets the complete stats from a given short URL.

        Args:
            short_url: short url requesting full registered URL.
        Returns:
            Complete URL stats.
        Raises:
            cherrypy.HTTPError: raises 404 if short url does not exist.
        """
        try:
            link = log_db.Log.stats(short_url)
        except url_db.UrlDoesNotExistException:
            raise cherrypy.HTTPError(404, f'Link {short_url} does not exist.')
        else:
            return link


class Total(base_api.Api):

    exposed = True

    @auth.header_auth
    def _get(self):
        return log_db.Log.totals()
