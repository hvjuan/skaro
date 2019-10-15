"""Main Skaro Handlers."""

import os

import cherrypy
import sqlalchemy
from sqlalchemy import exc as sa_exc
from sqlalchemy.orm import sessionmaker

from db import log as log_db
from db import url as url_db
import settings


engine = sqlalchemy.create_engine(settings.DB_URL_CONN)


class DatabaseNotReadyException(Exception):
    """Raised if Database is not ready."""


class Skaro:
    """Main Skaro class."""

    @cherrypy.expose
    def init_db(self):
        """Initializes/upgrades database.

        This needs to be run after docker finilizes starting all instances.

        TODO(juan) this should be in another module to avoid having this name
            used in any way as a short URL.
        """
        session = sessionmaker()
        session.configure(bind=engine)
        session = session()
        # Check that there's access to the DB with a simple query.
        try:
            results = session.query(url_db.Url).count()
            return f'Database is ready: {results}'
        except sa_exc.OperationalError:
            return f'Database is not ready yet. Try again later'
        finally:
            os.system('alembic upgrade head')

    @cherrypy.expose
    def default(self, short_url=None):
        """Forwarder index.

        Args:
            short_url: short url to be transformed into a full URL to be
                forwarded.
        Raises:
            cherrypy.HTTPRedirect: redirect if we got an URL successfully.
            cherrypy.HTTPError: raised as 404 if short url does not exist or
                if we visit root without any parameters.
        """

        if not short_url:
            raise cherrypy.HTTPError(404, 'You need a short URL.')
        # Redirector.
        try:
            forward_to = url_db.Url.get_url(short_url)
        except url_db.UrlDoesNotExistException:
            raise cherrypy.HTTPError(404, f'Link {short_url} does not exist.')
        else:
            # Log and redirect
            log_db.Log.add(forward_to.get('id'), cherrypy.request.remote.ip)
            raise cherrypy.HTTPRedirect(forward_to.get('url'))
