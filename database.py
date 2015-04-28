#############################################################################################
#           File: database.py                                                               #
#           Created By: Tal Rojansky - tulkinrb@gmail.com                                   #
#           Last Update: 5/2/15                                                             #
#############################################################################################


import config
import mysql.connector
from mysql.connector import errorcode

def connect():

    """connect to the database with properties of config modle, return connection and cursor"""

    try:
        conn = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.database, port=config.port)
    except mysql.connector.errors.InterfaceError as err:
        print("Error connecting to the database:\n" + str(err))
        ans = input("try again? (Y/N)\n")
        if ans.lower() == "y":
            return connect()
        return False # invaild input interpreted as no
    else:
        cursor = conn.cursor()
        return conn, cursor

class MySQLCursorSafe(mysql.connector.cursor.MySQLCursor):

    """A cursor with safe execute

    if executing a query when the connection was lost,
    the cursor will reconnect instead of raising exception
    """

    def __init__(self, connection):

        mysql.connector.cursor.MySQLCursor.__init__(self, connection)

    def execute(self, operation, params=None, multi=False):

        """safe execute"""

        try:
            return mysql.connector.cursor.MySQLCursor.execute(self, operation, params, multi)
        except mysql.connector.errors.OperationalError:
            try:
                self._connection.reconnect(attempts=3)
            except mysql.connector.errors.InterfaceError as err:
                print("Lost connection to database, error reconnecting:\n" + str(err))
                return False
            else:
                return mysql.connector.cursor.MySQLCursor.execute(self, operation, params, multi)

    def executemany(self, operation, seq_params):

        """safe executemany"""

        try:
            return mysql.connector.cursor.MySQLCursor.executemany(self, operation, seq_params)
        except mysql.connector.errors.OperationalError:
            try:
                self._connection.reconnect(attempts=3)
            except mysql.connector.errors.InterfaceError as err:
                print("Lost connection to database, error reconnecting:\n" + str(err))
                return False
            else:
                return mysql.connector.cursor.MySQLCursor.executemany(self, operation, seq_params)

        
