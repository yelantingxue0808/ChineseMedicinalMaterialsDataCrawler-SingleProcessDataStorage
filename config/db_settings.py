"""
@Author  : 孔天宇
@Desc    :
"""

class DbConfig:
    MYSQL = 0
    MONGODB = 1
    REDIS = 2


DB_CONNECT_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'text3'
}

DATABASE_DEFAULT_TYPE = DbConfig.MYSQL

