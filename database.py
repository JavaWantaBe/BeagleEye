__author__ = 'richard'

import _mysql
import logging
from settings import SettingManager

mysqlLogger = logging.getLogger('database')
dbsettings = SettingManager()


def insert_new_data(query):
    try:
        setting = dbsettings.get_settings('database')
        db = _mysql.connect(setting.get('host'), setting.get('user'),
                            setting.get('password'), setting.get('database'))
        db.query(query)
        db.close()
        mysqlLogger.info("New record inserted")
    except _mysql.DatabaseError:
        print "stuff"
        mysqlLogger.error("Database could not connect")


def test_database():
    insert_new_data("SHOW DATABASES")


if __name__ == "__main__":
    test_database()
