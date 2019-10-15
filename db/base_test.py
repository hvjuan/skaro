"""Base DB Tests."""

import unittest

import sqlalchemy.orm

import db
from utils import db_utils

# Test DB properties.
DB_URL_CONN = 'sqlite:///:memory:'
# Set echo to True if more DB debugging is needed.
_ENGINE = sqlalchemy.create_engine(DB_URL_CONN, echo=False)
_BASE = db.ModelBase

# Need to mock declarative base before importing.
db_utils.engine = _ENGINE


class TestBasis(unittest.TestCase):
    """Test basis for all DB modules.

    Ensures that a new db is created and
    destroyed for every test to achieve complete independence on every
    unit test.
    """

    def setUp(self):
        # Create test database tables.
        _BASE.metadata.create_all(_ENGINE)

    def tearDown(self):
        # Drop all tables on every test.
        _BASE.metadata.drop_all(_ENGINE)
