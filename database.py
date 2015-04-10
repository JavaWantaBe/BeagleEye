__author__ = 'richard'

import _mysql
import logging

mysqlLogger = logging.getLogger('database')

class Database:
    host = '127.0.0.1'
    def __init__(self, **kwargs):
        # ********************* Database Params ******************
        self.host = kwargs['host']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.database = kwargs['database']
        self.db = _mysql.connect()

    def request(self, query):
        try:
            self.db = _mysql.connect(self.host, self.user, self.password, self.database)
            return True
        except _mysql.Error, e:
            return False
        finally:
            print("Yep")

    def updateRequest(self, query):
        try:
            self.db = _mysql.connect( self.host, self.user, self.password, self.database )
        except _mysql.Error:
            mysqlLogger.error("Could not connect to database")

    