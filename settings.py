"""Project Skaro. URL Shortener."""

import os

import cherrypy


VERSION = '0.1'

# Front End.
FE_HOST = os.environ.get('FE_HOST', '')

# Database.
DB_USER = os.environ.get('DB_USER', 'skaro')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'skaro_pass')
DB_HOST = os.environ.get('DB_HOST', 'skaro_mysql')
DB_NAME = os.environ.get('DB_NAME', 'skaro')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_URL_CONN = u'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

# Test access key. TODO(juan) Should be replaced with an auth system.
ACCESS_KEY = 'HSHAGjqsqHSnnHDW2812_&&&'

# Web Server.
HOST = '0.0.0.0'
PORT = 9999
URL = 'http://qn.co.ve'

PATHS = {
    '/': {
        'tools.sessions.on': True,
        'tools.sessions.name': 'Gallifrey',
        'request.show_tracebacks': False,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    },

    # APIs.
    '/api': {
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [
            ('Content-Type', 'application/json')],
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    },
}

# Cherrypy global config params.
GLOBAL_CONF = {
    'server.socket_host': HOST,
    'server.socket_port': PORT,
}
