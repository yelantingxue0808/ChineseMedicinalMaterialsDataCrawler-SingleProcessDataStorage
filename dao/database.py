"""
@Author  : 孔天宇
@Desc    :
"""

import pymysql
from config import db_settings


# 单例设计模式（一个类只对应一个对象）

class Database:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            return super().__new__(cls)
        return cls.__instance

    def __init__(self, db_type=db_settings.DATABASE_DEFAULT_TYPE):
        self.db_type = db_type
        self.db_con = None

    def get_database_connect(self):
        mysql_config = db_settings.DB_CONNECT_CONFIG
        return pymysql.connect(host=mysql_config['host'],
                               user=mysql_config['user'],
                               password=mysql_config['password'],
                               database=mysql_config['database']
                               )

    def get_conn(self):
        match self.db_type:
            case db_settings.DATABASE_DEFAULT_TYPE:
                self.db_con = self.get_database_connect()
        return self.db_con
        # if self.db_type == db_settings.DATABASE_DEFAULT_TYPE:
        #     self.db_con = self.get_database_connect()
        #     return self.db_con
        # else:
        #     return self.db_con
