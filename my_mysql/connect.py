import mysql.connector
from conf import AppConfig

# 在模块中定义一个私有变量，用于存储单例对象
# _mysql_connect = None

def createMysqlConnect():
    # global _mysql_connect

    # 如果对象已经创建，则直接返回
    # if _mysql_connect is not None:
    #     return _mysql_connect

    # 创建连接对象
    _mysql_connect = mysql.connector.connect(user=AppConfig.mysql_username,
                                  password=AppConfig.mysql_user_password,
                                  host=AppConfig.mysql_host,
                                  database=AppConfig.db_name_001)

    return _mysql_connect