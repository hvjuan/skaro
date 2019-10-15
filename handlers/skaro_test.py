"""Tests for main."""

import logging
import unittest
from unittest import mock

import cherrypy
import webtest

from db import url as url_db
import settings
from handlers import skaro as skaro_handlers


# No logging to the screen on testing.
logging.getLogger("cherrypy").propagate = False
cherrypy.log.screen = False

_MOCKED_URL = {
    'id': 1,
    'short_url': 'mocked',
    'url': 'http://google.com'
}


class WebTestBasis(unittest.TestCase):

    def setUp(self):
        app = cherrypy.tree.mount(
            skaro_handlers.Skaro(), '/', config=settings.PATHS)
        self.testapp = webtest.TestApp(app)

    def tearDown(self):
        cherrypy.engine.exit()

    @mock.patch.object(skaro_handlers.log_db, 'Log', autospec=True)
    @mock.patch.object(skaro_handlers.url_db, 'Url', autospec=True)
    def test_redirect(self, mocked_url, mocked_log):
        mocked_url.get_url.return_value = _MOCKED_URL
        response = self.testapp.get('/not_mocked')
        # Test for redirection and that the log method was called.
        self.assertEqual(302, response.status_int)
        self.assertTrue(mocked_log.add.call_args())

    def test_redirect__no_link_raises_404_(self):
        response = self.testapp.get('/', status='*')
        self.assertEqual(404, response.status_int)

    @mock.patch.object(skaro_handlers.url_db, 'Url', autospec=True)
    def test_redirect__no_short_url_raises_404_(self, mocked_url):
        mocked_url.get_url.side_effect = url_db.UrlDoesNotExistException
        response = self.testapp.get('/i_dont_exist', status='*')
        self.assertEqual(404, response.status_int)


if __name__ == '__main__':
    unittest.main()
