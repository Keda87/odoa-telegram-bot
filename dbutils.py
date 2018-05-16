import sqlite3

from skylark import Model, Field, Database


class Subscriber(Model):
    telegram_id = Field()
    username = Field()
    first_name = Field()
    last_name = Field()


class DBUtils(object):

    def __init__(self, db_name):
        Database.set_dbapi(sqlite3)
        Database.config(db=db_name)

    def insert(self, telegram_id, username, first_name, last_name):
        try:
            meta = {
                'telegram_id': telegram_id,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
            }
            Subscriber.create(**meta)
            return True
        except sqlite3.IntegrityError:
            return False

    def get(self, telegram_id):
        return Subscriber.findone(telegram_id=telegram_id)

    def delete(self, telegram_id):
        subscriber = self.get(telegram_id=telegram_id)
        if subscriber:
            subscriber.destroy()
            return True
        return False

    def fetch_all(self):
        return Subscriber.select(Subscriber.telegram_id)

