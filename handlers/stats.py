"""Main Stats Handlers."""

import cherrypy

from db import log as log_db


class Stats:
    """Main Stats class."""

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def default(self, short_url):
        """Stats index.

        Args:
        """
        return log_db.Log.stats(short_url)
