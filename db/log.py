"""Skaro URL Shortener log Model."""

import datetime

import sqlalchemy
from sqlalchemy import orm

from db import ModelBase
from db import url as url_db
from utils import db_utils


class Log(ModelBase):
    """Skaro URLs logs Model."""

    __tablename__ = 'log'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    url_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey(url_db.Url.id),
                               nullable=False)
    ip = sqlalchemy.Column(sqlalchemy.String(16))
    activity_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=lambda *x: datetime.datetime.now())
    url = orm.relationship(url_db.Url, backref='logs')

    @classmethod
    def add(cls, url_id, ip):
        """Creates a log instance to track traffic activity.

        Args:
            url_id: URL.id foreign key.
            ip: IP address that accessed the redirection.
        """
        new_log = cls()
        with db_utils.session_scope() as session:
            new_log.url_id = url_id
            new_log.ip = ip
            session.add(new_log)

    @classmethod
    def stats(cls, short_url):
        """Get stats from given url id."""
        url = url_db.Url.get_url(short_url)
        # Get short link created and get times it has been visited.
        stats = {
            'url': url.get('url'),
            'short_url': url.get('short_url'),
            'creation_date': str(url.get('creation_date')),
            # TODO(juan) this is a simple count to all children. This can
            # be automated on deferred tasks to avoid doing a linear count
            # every time.
            'times_visited': len(url.get('logs'))
        }
        # Historagram: visits to short link per day.
        # TODO(juan) done on the fly for demo purposes. This should be
        # porcessed outside of the function on a deferred task.
        with db_utils.session_scope() as session:
            response = session.query(
                sqlalchemy.func.count(cls.activity_date),
                sqlalchemy.func.date(cls.activity_date)
            ).filter_by(url_id=url.get('id')).group_by(
                sqlalchemy.func.date(cls.activity_date)).all()

            return {
                'stats': stats,
                'historagram': [{'visits': str(x), 'date': str(y)}
                                for x, y in response]
            }

    @classmethod
    def totals(cls):
        """Get total of visits ordered by short url.

        TODO(juan) No pagination is done. This is just for demo purposes.

        Returns:
            list of short urls with number of individual visits.
        """
        with db_utils.session_scope() as session:
            urls = session.query(url_db.Url).all()
            # Get all logs per url.
            return [{x.short_url: len(x.logs)} for x in urls]

    def to_dict(self):
        """Returns a dictionary representation od the current instance."""
        return {
            'id': self.id,
            'url_id': self.url_id,
            'url': self.url.url,
            'ip': self.ip,
            'activity_date': str(self.activity_date)
        }

    def __repr__(self):
        return f'<Log(id={self.id})>'
