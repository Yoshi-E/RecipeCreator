from flask_mysqldb import MySQL
from Webserver.static.py.Log import log
from Webserver.static.py.Config import Config
from Webserver import app

import MySQLdb
import MySQLdb.cursors

cfg = Config("Webserver\static\config\database.json",
                "Webserver\static\config\database.json_default")

#Contexbased DB:
app.config['MYSQL_HOST'] = cfg["host"]
app.config['MYSQL_USER'] = cfg["user"]
app.config['MYSQL_PASSWORD'] = cfg["password"]
#app.config['MYSQL_DB'] = cfg["database"]
app.config['MYSQL_PORT'] = cfg["port"]
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

db = MySQL(app)

class Database(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self.__connect(cfg)

    def __connect(self, cfg):
        self.db = MySQLdb.connect(host=cfg["host"],
                        user=cfg["user"],     
                        passwd=cfg["password"],
                        #db=cfg["database"],
                        port=cfg["port"],
                        cursorclass=MySQLdb.cursors.DictCursor)
        self.db_cursor = self.db.cursor()

    def exe_sql(self, sql, cursor=None):
        if(db.connection):
            cur = db.connection.cursor()
            try:
                cur.execute(sql)
                db.connect.commit()
                return cur.fetchall()
            except Exception as ex:
                log.info(sql)
                log.print_exc()
                db.connection.rollback()
                raise Exception("Error: {}: {}".format(sql, ex))
        else: #using non context based SQL
            cur = cursor
            if(not cursor):
                cur = self.db.cursor()  

            try:
                cur.execute(sql)
                self.db.commit()
                return cur.fetchall()
            except Exception as ex:
                log.info(sql)
                log.print_exc()
                self.db.rollback()
                raise Exception("Error: {}: {}".format(sql, ex))

from .ingredients import DatabaseIngredients
from .topics import TopicManager