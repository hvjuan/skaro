"""URL API."""

import cherrypy

from api import base_api
from db import url as url_db
from utils import auth
import settings


class Url(base_api.Api):

    exposed = True

    @auth.header_auth
    def _get(self, short_url):
        """Gets the complete object from a given short URL.

        Args:
            short_url: short url requesting full registered URL.
        Returns:
            Complete URL dictionary if exists.
        Raises:
            cherrypy.HTTPError: raises 404 if short url does not exist.
        """
        try:
            link = url_db.Url.get_url(short_url)
        except url_db.UrlDoesNotExistException:
            raise cherrypy.HTTPError(404, f'Link {short_url} does not exist.')
        else:
            return link

    def _post(self, url, short_url=None):
        """Creates a new, short URL from a given full URL.

        Args:
            url: url to have the new shortened link. If the given URL already
                has a short and not custom URL, it will be returned.
            short_url: if present, will create the custom link/name provided.
                It will enable up to the same allowed characters, if it's
                longer, the string will be truncated.
        Returns:
            Newly created short URL.
        """
        short_link = url_db.Url.create(url, short_url)
        return f'{settings.URL}/{short_link}'
