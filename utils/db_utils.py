"""Database utils."""

from contextlib import contextmanager
import logging

import sqlalchemy
from sqlalchemy.orm import sessionmaker

import settings


engine = sqlalchemy.create_engine(settings.DB_URL_CONN)


@contextmanager
def session_scope():
    """Create a SQLAlchemy session scoppe with a Context Manager.

    Yields:
        SQLAlchemy session.
    Raises:
        DatabaseNotReadyException: if database is not ready. Will sync alembic.
    """
    # Create session.
    session = sessionmaker()
    session.configure(bind=engine)
    session = session()

    try:
        yield session
        session.commit()

    # Rollback on any exception.
    except Exception as e:
        logging.info('Rollback: %s', e)
        session.rollback()
        raise
    # Close no matter what.
    finally:
        session.close()
