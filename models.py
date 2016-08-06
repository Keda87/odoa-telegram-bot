import sqlite3
from skylark import Database
from skylark import Model, Field


class Subscriber(Model):
    telegram_id = Field()
    username = Field()
    first_name = Field()
    last_name = Field()
    message = Field()


Database.set_dbapi(sqlite3)
Database.config(db='odoa')
