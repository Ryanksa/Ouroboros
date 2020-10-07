import os
import pg8000 as pg
from error import Error
from utils import print_sys, print_curr

class Shell:
    def __init__(self, dbHost, dbUser, dbPassword, dbName, port):
        # DB variables
        self.connection = pg.connect(host=dbHost, user=dbUser, password=dbPassword, database=dbName, port=port)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS notes(name VARCHAR(128) NOT NULL, content text, grouping VARCHAR(128))""")
        # error handler
        self.err = Error()
        # other variables
        self.curr = ""
        self.opened = ""
        self.exit = False
