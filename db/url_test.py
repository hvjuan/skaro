"""Tests for Url model."""

import unittest

from db import base_test
# Needed to be in the environment so it can be loaded in the test db.
from db import log as log_db  # NOQA W0611
from db import url as url_db


class UrlTest(base_test.TestBasis):

    def test_create(self):
        # Check that it returns first a short url with the same lenght as the
        # module.
        short_url = url_db.Url.create('http://google.com')
        self.assertEqual(url_db.MAX_CHARACTERS, len(short_url))

    def test_create__short_link_already_exists(self):
        # Create it once.
        first = url_db.Url.create('http://google.com')
        # but checking coverage will show that it returns from the response.
        second = url_db.Url.create('http://google.com')
        self.assertEqual(first, second)

    def test_create__custom_redirect(self):
        short_url = url_db.Url.create('http://google.com/long_url', 'short')
        self.assertEqual('short', short_url)

    def test_create__custom_redirect_already_exists(self):
        # First test.
        short_url = url_db.Url.create('http://google.com/long_url', 'short')
        self.assertEqual('short', short_url)
        # Create again, should return the same. Checking with coverage, will
        # return the same.
        short_url = url_db.Url.create('http://google.com/long_url', 'short')
        self.assertEqual('short', short_url)

    def test_create__custom_redirect_longer_string(self):
        short_url = url_db.Url.create('http://google.com/long_url',
                                      '1234567890')
        self.assertEqual('1234567', short_url)

    def test_get(self):
        # Create normal url and test it.
        url_db.Url.create('http://google.com')
        # Get.
        response = url_db.Url.get('http://google.com')
        self.assertEqual('http://google.com', response.url)
        self.assertEqual(7, len(response.short_url))

    def test_get__custom_url(self):
        # Create.
        url = 'http://google.com/long_url/long.html'
        url_db.Url.create(url, 'custom')
        # Get.
        response = url_db.Url.get(url, 'custom')
        self.assertEqual(url, response.url)
        self.assertEqual('custom', response.short_url)

    def test_get_url(self):
        # Create a new link to be tested lated.
        short_url = url_db.Url.create('http://google.com')
        # Now get the short link directly and compare.
        full_url = url_db.Url.get_url(short_url)
        self.assertEqual('http://google.com', full_url.get('url'))

    def test_get_url__generates_exception(self):
        msg = 'Given url "dont" is not registered.'
        with self.assertRaisesRegex(url_db.UrlDoesNotExistException, msg):
            url_db.Url.get_url('dont')

    def test_generate(self):
        # It should generate a random string of the same length specified in
        # the module.
        short_url = url_db.Url.generate()
        self.assertEqual(url_db.MAX_CHARACTERS, len(short_url))

    def test_repr(self):
        url_db.Url.create('http://google.com')
        response = url_db.Url.get('http://google.com')
        self.assertEqual('<URL(id=1, url=http://google.com)>',
                         str(response))


if __name__ == '__main__':
    unittest.main()
