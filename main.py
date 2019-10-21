"""Project Skaro. URL Shortener."""

import logging

import cherrypy

from api import stats as stats_api
from api import url as url_api
from handlers import skaro as skaro_handlers
import settings


# Mounting routes.
root = skaro_handlers.Skaro()

# APIs.
root.api = type('SkaroAPIs', (), {})
root.api.url = url_api.Url()
root.api.stats = type('SkaroAPIs', (), {})
root.api.stats.url = stats_api.Stats()
root.api.stats.totals = stats_api.Total()

cherrypy.tree.mount(root, '/', config=settings.PATHS)
cherrypy.log('Starting Skaro server')
logging.getLogger("cherrypy").propagate = False

# Global Server config.
cherrypy.config.update(settings.GLOBAL_CONF)
