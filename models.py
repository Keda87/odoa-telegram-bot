import pymysql
from ConfigParser import RawConfigParser
from skylark import Database
from skylark import Model, Field


class Subscriber(Model):
    telegram_id = Field()
    username = Field()
    first_name = Field()
    last_name = Field()
    message = Field()

config = RawConfigParser()
config.read('config.ini')

db_name = config.get('main', 'db_name')
db_user = config.get('main', 'db_user')
db_pass = config.get('main', 'db_pass')

Database.set_dbapi(pymysql)
Database.config(db=db_name, user=db_user, passwd=db_pass)
