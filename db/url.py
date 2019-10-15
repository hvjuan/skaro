"""Skaro URL Shortener Model."""

import datetime
import random

import sqlalchemy

from db import ModelBase
from utils import db_utils
import settings

engine = sqlalchemy.create_engine(settings.DB_URL_CONN)
MAX_CHARACTERS = 7
_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class ShortUrlAlreadyExistsException(Exception):
    """Raised if we are trying to get a shortend url already used."""


class UrlDoesNotExistException(Exception):
    """Raised if we look for an URL that does not have a short link."""


class Url(ModelBase):
    """Skaro URLs Model."""

    __tablename__ = 'url'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    # Custom: if true, means the user chose the url name.
    custom = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    url = sqlalchemy.Column(sqlalchemy.String(512), index=True)
    short_url = sqlalchemy.Column(sqlalchemy.String(16), index=True)
    creation_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now())

    @classmethod
    def create(cls, url, short_url=None):
        """Creates a new short URL for a given link.

        Current rule: URLs can only have one short generated URL but
            can have many custom ones.

        Args:
            url: url to have the new shortened link. If the given URL already
                has a short and not custom URL, it will be returned.
            short_url: if present, will create the custom link/name provided.
                It will enable up to the same allowed characters, if it's
                longer, the string will be truncated.
        Returns:
            Newly created short URL.
        """
        with db_utils.session_scope() as session:
            # Generating short URL.
            if not short_url:
                # Check that the URL doesn't already have one.
                response = cls.get(url)
                if not response:
                    # Create new short URL.
                    new_url = cls()
                    new_url.url = url
                    new_url.short_url = cls.generate()
                    session.add(new_url)
                    session.commit()
                    return new_url.short_url
                # It already had one, so we get it.
                return response.short_url
            # Custom URL.
            # Check if it exists.
            response = cls.get(url=url, short_url=short_url)
            if response:
                return response.short_url
            # Create one as it doesn't exist.
            new_url = cls()
            new_url.url = url
            # Truncates all custom short urls to the max allowed characters.
            new_url.short_url = short_url[:MAX_CHARACTERS]
            new_url.custom = True
            session.add(new_url)
            return new_url.short_url

    @classmethod
    def get(cls, url, short_url=None):
        """Gets all existing data from a given URL and short_url.

        Args:
            url: url to query.
            short_url: if present, will check for custom URL.
        Returns:
            Dictionary with all the requested data.
        """
        with db_utils.session_scope() as session:
            kwargs = {'url': url}
            if short_url:
                kwargs.update({'short_url': short_url})
            response = session.query(cls).filter_by(**kwargs).first()
            if response:
                session.expunge_all()
                return response

    @classmethod
    def get_url(cls, short_url):
        """Gets a dictionary representation from a given short URL.

        Args:
            short_url: short url requesting full registered URL.
        Returns:
            Complete URL dictionary if exists.
        Raises:
            UrlDoesNotExistException: raised if given a short url that does
                not exist in the table.
        """
        with db_utils.session_scope() as session:
            url = session.query(cls).filter_by(short_url=short_url).first()
            if not url:
                raise UrlDoesNotExistException(
                    f'Given url "{short_url}" is not registered.')
            return url.to_dict()

    @classmethod
    def generate(cls):
        """Creates a new short url for a given path.

        This uses a randon character for every position till it reaches the
        given limit on MAX_CHARACTERS.

        This is the chosen approach for this coding exercise. Other approaches
        may include using a base62 range to elaborate random characters but
        in the meantime, we can depend on indexed columns for checking existing
        values. We will be using 62 characters with 7 positions, making it
        possible to have over a trillion combinations (62^7.)

        My issue with not having fully randomized URLs is that, depending on
        the main requirement, it could be easily guessed by someone, posing
        a possible threat to any confidential URL (of course, if that is
        something to be considered.) Of course, this approach may be discussed
        that is not totally random/pseudorandom but, for this excercise,
        checking current links can be fairly quick as searches on indexed
        columns are fast.

        Depending on how we need to scale the solution (high qps, availability,
        and other factors), we could also have a different approach using
        NoSQL databases.

        Returns:
            Newly generated short URL.
        """
        with db_utils.session_scope() as session:
            # Use only one connection session. Retry if a duplicate is found.
            while True:
                short_url = ''.join(random.choice(_CHARS)
                                    for i in range(MAX_CHARACTERS))
                if not session.query(cls).filter_by(
                        short_url=short_url).first():
                    return short_url

    def to_dict(self):
        """Returns a dictionary from a current instance.

        TODO(juan) Logs can indeed be preprocessed or chosen not to be added.
        """
        return {
            'id': self.id,
            'custom': self.custom,
            'url': self.url,
            'short_url': self.short_url,
            'creation_date': str(self.creation_date),
            'logs': [x.to_dict() for x in self.logs if x]
        }

    def __repr__(self):
        return f'<URL(id={self.id}, url={self.url})>'
