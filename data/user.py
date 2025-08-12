import datetime

import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    auth_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    subed = sqlalchemy.Column(sqlalchemy.Boolean)
    shiki_access_token =  sqlalchemy.Column(sqlalchemy.String)
    shiki_refresh_token = sqlalchemy.Column(sqlalchemy.String)
    shiki_user_id = sqlalchemy.Column(sqlalchemy.Integer)


    def __repr__(self):
        return f'<User> id - {self.id}; '
