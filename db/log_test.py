"""Tests for Log model."""

import unittest

from db import base_test
from db import log as log_db
from db import url as url_db


class LogTest(base_test.TestBasis):

    def test_add(self):
        # Create link to have proper IDs.
        url_db.Url.create('http://google.com')
        # Get object from db and create a log.
        url = url_db.Url.get('http://google.com')
        log_db.Log.add(url.id, '192.168.192.200')
        # Get logs from given url. Get them again.
        url = url_db.Url.get_url(url.short_url)
        self.assertEqual(1, len(url.get('logs')))
        self.assertEqual('http://google.com', url.get('logs')[0].get('url'))

    def test_stats(self):
        # Create link to have proper IDs.
        url_db.Url.create('http://google.com')
        # Get object from db and create a couple of logs from different ips.
        url = url_db.Url.get('http://google.com')
        log_db.Log.add(url.id, '192.168.192.200')
        log_db.Log.add(url.id, '192.168.192.201')
        log_db.Log.add(url.id, '192.168.192.202')
        stats = log_db.Log.stats(url.short_url)
        # There should be 3 visits from different IPs consolidated into one
        # day.
        self.assertEqual('3', stats.get('historagram')[0].get('visits')[0])
        # Stats.
        self.assertEqual('http://google.com', stats.get('stats').get('url'))


if __name__ == '__main__':
    unittest.main()
