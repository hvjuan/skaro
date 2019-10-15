"""Project Skaro. URL Shortener."""

import logging

import cherrypy

from api import url as url_api
from handlers import skaro as skaro_handlers
from handlers import stats as stats_handlers
import settings


# Mounting routes.
root = skaro_handlers.Skaro()
root.stats = stats_handlers.Stats()

# APIs.
root.api = type('SkaroAPIs', (), {})
root.api.url = url_api.Url()

cherrypy.tree.mount(root, '/', config=settings.PATHS)
cherrypy.log('Starting Skaro server')
logging.getLogger("cherrypy").propagate = False

# Global Server config.
cherrypy.config.update(settings.GLOBAL_CONF)
