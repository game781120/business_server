import json

import mysql.connector
from conf.conf import AppConfig
from my_log.mylogger import logger

# 在模块中定义一个私有变量，用于存储单例对象
_mysql_connect = None


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


def inserData(cnx, data):
    # 创建游标对象
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO wenshu (uuid,original_link,case_num,case_name"
        ",court,area,case_type,case_type_code"
        ",source,trial,referee_date,public_date"
        ",case_personnel,case_reason,legal_basis"
        ",full_text)"
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

    new_data = ()
    i = 0
    for d in data:
        i += 1
        new_data = new_data + (f'{d}',)
    # 执行插入操作
    cursor.execute(insert_stmt, new_data)

    # 提交事务
    cnx.commit()

    # 关闭游标和连接
    cursor.close()


def query_wenshu_all():
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行 SQL 查询
    query = 'SELECT uuid,case_reason,full_text FROM wenshu'
    cursor.execute(query)

    # 获取结果
    data_dict = {}
    for row in cursor:
        uuid = row[0]
        case_reason = row[1]
        full_text = row[2]
        data_dict.update({uuid: {"case_reason": case_reason, "full_text": full_text}})
    # 关闭游标和连接
    cursor.close()

    return data_dict


def query_wenshu_by_case_num_case_name(case_num, case_name):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行 SQL 查询
    query = (f"SELECT uuid FROM wenshu"
             f" where case_num = '{case_num}' and  case_name= '{case_name}'")
    cursor.execute(query)

    # 获取结果
    uuid = None
    for row in cursor:
        uuid = row[0]

    # 关闭游标和连接
    cursor.close()

    return True if uuid else False


def query_wenshu_like_info_by_uuid(uuid):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行 SQL 查询
    query = f"select uuid,case_reason,full_text  from wenshu where  uuid = '{uuid}'"
    print(f"query_wenshu_like_info_by_uuid query={query}")
    cursor.execute(query)

    # 获取结果
    data_dict = {}
    for row in cursor:
        uuid = row[0]
        case_reason = row[1]
        full_text = row[2]
        data_dict.update({uuid: {"case_reason": case_reason, "full_text": full_text}})
    # 关闭游标和连接
    cursor.close()

    # print(f"data_dict={data_dict}")
    return data_dict


def query_wenshu_like_info_by_case_reason(case_reason):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行 SQL 查询
    query = f"select uuid,case_reason,full_text  from wenshu where  case_reason  like  '%{case_reason}%'"
    print(f"query_wenshu_like_info_by_case_reason query={query}")
    cursor.execute(query)

    # 获取结果
    data_dict = {}
    for row in cursor:
        uuid = row[0]
        case_reason = row[1]
        full_text = row[2]
        data_dict.update({uuid: {"case_reason": case_reason, "full_text": full_text}})
    # 关闭游标和连接
    cursor.close()

    return data_dict


def query_wenshu_second_all():
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行 SQL 查询
    query = 'SELECT uuid,type_name,content,is_es,is_milvus,is_model,is_mysql FROM wenshu_second'
    cursor.execute(query)

    # 获取结果
    data_dict = {}
    for row in cursor:
        uuid = row[0]
        type_name = row[1]
        content = row[2]
        is_es = row[3]
        is_milvus = row[4]
        is_model = row[5]
        is_mysql = row[6]
        data_dict.update(
            {
                uuid:
                    {
                        "type_name": type_name,
                        "content": content,
                        "is_es": is_es,
                        "is_milvus": is_milvus,
                        "is_mysql": is_mysql,
                        "is_model": is_model,
                    }
            }
        )
    # 关闭游标和连接
    cursor.close()

    return data_dict


def query_wenshu_second_by_uuid(uuid):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    query = f'SELECT uuid,type_name,content,is_es,is_milvus,is_model,is_mysql FROM wenshu_second WHERE uuid = "{uuid}"'
    cursor.execute(query)
    rows = cursor.fetchall()
    data_dict = {}
    for row in rows:
        uuid = row[0]
        type_name = row[1]
        content = row[2]
        is_es = row[3]
        is_milvus = row[4]
        is_model = row[5]
        is_mysql = row[6]
        data_dict.update(
            {
                uuid:
                    {
                        "type_name": type_name,
                        "content": content,
                        "is_es": is_es,
                        "is_milvus": is_milvus,
                        "is_mysql": is_mysql,
                        "is_model": is_model,
                    }
            }
        )
    # 关闭游标
    cursor.close()
    return data_dict


def query_wenshu_case_type():
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    query = f'select case_reason from wenshu group by case_reason'
    cursor.execute(query)
    rows = cursor.fetchall()
    res = []
    if rows:
        for row in rows:
            print(f"wenshu case_type ={row[0]}")
    # 关闭游标
    cursor.close()
    return res


def query_wenshu_second_case_type():
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    query = f'select type_name from wenshu_second group by type_name'
    cursor.execute(query)
    rows = cursor.fetchall()
    res = []
    if rows:
        for row in rows:
            print(f"wenshu_second case_type ={row[0]}")
    # 关闭游标
    cursor.close()
    return res


def query_wenshu_third_case_type():
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    query = f'select type_name from wenshu_third group by type_name'
    cursor.execute(query)
    rows = cursor.fetchall()
    res = []
    if rows:
        for row in rows:
            print(f"wenshu_third case_type ={row[0]}")
    # 关闭游标
    cursor.close()
    return res


def insert_wenshu_second_v2(uuid, type_name, content):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO wenshu_second (uuid,type_name,content,is_model)"
        "VALUES (%s,%s,%s,%s)")

    new_data = (uuid, type_name, content, 1)
    logger.info(f"insert_wenshu_second_v2={new_data}")
    cursor.execute(insert_stmt, new_data)

    # 提交事务
    cnx.commit()

    # 关闭游标和连接
    cursor.close()


# def insert_wenshu_second_v2(uuid,type_name,content):
#
#     cnx = createMysqlConnect()
#     # 创建游标对象
#     cursor = cnx.cursor()
#     insert_stmt = (
#         "INSERT INTO wenshu_second (uuid,type_name,content,is_model)"
#         "VALUES (%s,%s,%s,%s)")
#
#     new_data = (uuid, type_name, content, 1)
#     logger.info(f"insert_wenshu_second_v2={new_data}")
#     cursor.execute(insert_stmt, new_data)
#
#     # 提交事务
#     cnx.commit()
#
#     # 关闭游标和连接
#     cursor.close()

def update_wenshu_second_v2(uuid, type_name, content):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    update_stmt = f"UPDATE wenshu_second SET type_name ='{type_name}', content ='{content}', is_model = 1 WHERE uuid ='{uuid}'"
    logger.info(f"update_wenshu_second_v2={update_stmt}")
    cursor.execute(update_stmt)
    # 提交事务
    cnx.commit()
    # 关闭游标
    cursor.close()


def update_wenshu_second_is_es(uuid):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    update_stmt = f"UPDATE wenshu_second SET is_es =1 WHERE uuid ='{uuid}'"
    logger.info(f"update_wenshu_second_is_es={update_stmt}")
    cursor.execute(update_stmt)
    # 提交事务
    cnx.commit()
    # 关闭游标
    cursor.close()


def update_wenshu_second_is_milvus(uuid):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    update_stmt = f"UPDATE wenshu_second SET is_milvus =1 WHERE uuid ='{uuid}'"
    logger.info(f"update_wenshu_second_is_milvus={update_stmt}")
    cursor.execute(update_stmt)
    # 提交事务
    cnx.commit()
    # 关闭游标
    cursor.close()


def update_wenshu_second_is_mysql(uuid):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    update_stmt = f"UPDATE wenshu_second SET is_mysql =1 WHERE uuid ='{uuid}'"
    logger.info(f"update_wenshu_second_is_mysql={update_stmt}")
    cursor.execute(update_stmt)
    # 提交事务
    cnx.commit()
    # 关闭游标
    cursor.close()


def query_wenshu_third_all():
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行 SQL 查询
    query = 'SELECT uuid,money FROM wenshu_third'
    cursor.execute(query)

    # 获取结果
    data_dict = {}
    for row in cursor:
        uuid = row[0]
        content = row[1]

        data_dict.update({uuid: {"content": content}})
    # 关闭游标和连接
    cursor.close()

    return data_dict


def query_wenshu_third_moeny_by_uuid(uuid):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    query = f'SELECT uuid,is_money,money FROM wenshu_third WHERE uuid = "{uuid}"'
    cursor.execute(query)
    rows = cursor.fetchall()
    res = []
    if rows:
        for row in rows:
            res = [row[0], row[1], row[2]]

    cursor.close()
    return res


def query_wenshu_third_by_info(case_type, money=None, article_money=None):
    if not money and not article_money:
        return None
    cnx = createMysqlConnect()

    max_money = 0
    min_money = 0
    max_article_money = 0
    min_article_money = 0

    if money:
        money = float(money)
        max_money = money * 1.2
        min_money = money * 0.8
        max_money_table = 0
        max_cursor = cnx.cursor()
        query_value = 'SELECT MAX(money) FROM wenshu_third'
        max_cursor.execute(query_value)
        rows = max_cursor.fetchall()
        if rows:
            for row in rows:
                max_money_table = row[0]
        # 关闭游标和连接
        max_cursor.close()
        if max_money > max_money_table:
            max_money = max_money_table
            if min_money >= max_money:
                min_money = max_money * 0.8

    if article_money:
        article_money = float(article_money)
        max_article_money = article_money * 1.2
        min_article_money = article_money * 0.8

        max_article_money_table = 0
        max_cursor = cnx.cursor()
        query_value = 'SELECT MAX(article_money) FROM wenshu_third'
        max_cursor.execute(query_value)
        rows = max_cursor.fetchall()
        if rows:
            for row in rows:
                max_article_money_table = row[0]
        # 关闭游标和连接
        max_cursor.close()
        if max_article_money > max_article_money_table:
            max_article_money = max_article_money_table
            if min_article_money >= max_article_money:
                min_article_money = max_article_money * 0.8

    print("整理后\n")
    print(f"max_money={max_money} min_money={min_money}")
    print(f"max_article_money={max_article_money} min_article_money={min_article_money}")

    res = []
    # 创建游标对象
    cursor = cnx.cursor()
    query = f"select uuid ,money ,article_money from  wenshu_third where type_name like '%{case_type}%' "
    if money and article_money:
        query += (f" and ((money >= {min_money} and money <= {max_money})"
                  f" and (article_money >= {min_article_money} and article_money <= {max_article_money}))")
    elif money:
        query += f" and (money >= {min_money} and money <= {max_money} and article_money=0)"
        # query += (f" and ((money >= {min_money} and money <= {max_money})"
        #           f" or (article_money >= {min_money} and article_money <= {max_money}))")
    elif article_money:
        query += f" and (article_money >= {min_article_money} and article_money <= {max_article_money} and money=0)"
        # query += (f" and ((money >= {min_article_money} and money <= {max_article_money})"
        #           f" or (article_money >= {min_article_money} and article_money <= {max_article_money}))")

    query += " limit 10"
    print(f"query={query}")
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"rows={rows}")
    if rows:
        for row in rows:
            res.append(row[0])
    cursor.close()
    return res


def query_wenshu_third_moeny_by_money(money):
    money = float(money)
    cnx = createMysqlConnect()

    max_money = money * 1.2
    min_money = money * 0.8

    min_money_table = 0
    max_money_table = 0
    min_cursor = cnx.cursor()
    min_query = 'SELECT MIN(money) FROM wenshu_third'
    min_cursor.execute(min_query)
    rows = min_cursor.fetchall()
    if rows:
        for row in rows:
            min_money_table = row[0]
    # 关闭游标和连接
    min_cursor.close()

    max_cursor = cnx.cursor()
    max_query = 'SELECT MAX(money) FROM wenshu_third'
    max_cursor.execute(max_query)
    rows = max_cursor.fetchall()
    if rows:
        for row in rows:
            max_money_table = row[0]
    # 关闭游标和连接
    max_cursor.close()
    print("原始\n")
    print(
        f"max_money={max_money} min_money={min_money} min_money_table={min_money_table} max_money_table={max_money_table}")

    if min_money < min_money_table:
        min_money = min_money_table
        if max_money <= min_money:
            max_money = min_money * 1.2

    if max_money > max_money_table:
        max_money = max_money_table
        if min_money >= max_money:
            min_money = max_money * 0.8

    print("整理后\n")
    print(
        f"max_money={max_money} min_money={min_money} min_money_table={min_money_table} max_money_table={max_money_table}")

    # 创建游标对象
    cursor = cnx.cursor()
    query = f'SELECT uuid FROM wenshu_third WHERE money >= "{min_money}" and money <= "{max_money}" and is_money = 1'
    print(f"query={query}")
    cursor.execute(query)
    rows = cursor.fetchall()
    res = []
    if rows:
        for row in rows:
            res = [row[0]]

    print(f"res={res}")
    return res


def insert_wenshu_third_money(uuid, money):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO wenshu_third (uuid,money,is_money)"
        "VALUES (%s,%s,%s)")

    new_data = (uuid, money, 1)
    print(f"insert_wenshu_third_money={new_data}")
    cursor.execute(insert_stmt, new_data)

    # 提交事务
    cnx.commit()

    # 关闭游标和连接
    cursor.close()


def insert_wenshu_third_info(uuid, type_name=None, money=None, article=None,
                             article_money=None,
                             case_personnel=None, case_tool=None, case_date=None,
                             location=None, judgment=None, punish_money=None,
                             zishou=None):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()

    insert_stmt01 = "INSERT INTO wenshu_third (uuid"
    insert_stmt02 = " VALUES (%s"
    values_data = (uuid,)
    if type_name:
        insert_stmt01 += ",type_name"
        insert_stmt02 += ",%s"
        values_data += (f'{type_name}',)

    if money:
        insert_stmt01 += ",money"
        insert_stmt02 += ",%s"
        values_data += (money,)
    if article:
        insert_stmt01 += ",article"
        insert_stmt02 += ",%s"
        values_data += (f'{article}',)
    if article_money:
        insert_stmt01 += ",article_money"
        insert_stmt02 += ",%s"
        values_data += (article_money,)

    if case_personnel:
        insert_stmt01 += ",case_personnel"
        insert_stmt02 += ",%s"
        values_data += (f'{case_personnel}',)
    if case_tool:
        insert_stmt01 += ",case_tool"
        insert_stmt02 += ",%s"
        values_data += (f'{case_tool}',)
    if case_date:
        insert_stmt01 += ",case_date"
        insert_stmt02 += ",%s"
        values_data += (f'{case_date}',)
    if location:
        insert_stmt01 += ",location"
        insert_stmt02 += ",%s"
        values_data += (f'{location}',)
    if judgment:
        insert_stmt01 += ",judgment"
        insert_stmt02 += ",%s"
        values_data += (f'{judgment}',)
    if punish_money:
        insert_stmt01 += ",punish_money"
        insert_stmt02 += ",%s"
        values_data += (punish_money,)
    if zishou:
        insert_stmt01 += ",zishou"
        insert_stmt02 += ",%s"
        values_data += (f'{zishou}',)

    insert_stmt01 += ")"
    insert_stmt02 += ")"

    insert_sql = insert_stmt01 + insert_stmt02

    print(f"insert_wenshu_third_info={insert_sql}")
    cursor.execute(insert_sql, values_data)
    # 提交事务
    cnx.commit()
    # 关闭游标和连接
    cursor.close()
    cnx.close()


def update_wenshu_third_info(uuid, type_name=None, money=None, article=None,
                             article_money=None,
                             case_personnel=None, case_tool=None,
                             case_date=None, location=None, judgment=None,
                             punish_money=None, zishou=None):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    update_stmt = f"UPDATE wenshu_third SET is_money = 1 "
    if type_name:
        update_stmt += f",type_name ='{type_name}'"
    if money:
        update_stmt += f",money ={money}"
    if article:
        update_stmt += f",article ='{article}'"
    if article_money:
        update_stmt += f",article_money ='{article_money}'"
    if case_personnel:
        update_stmt += f",case_personnel ='{case_personnel}'"
    if case_tool:
        update_stmt += f",case_tool ='{case_tool}'"
    if case_date:
        update_stmt += f",case_date ='{case_date}'"
    if location:
        update_stmt += f",location ='{location}'"
    if judgment:
        update_stmt += f",judgment ='{judgment}'"
    if punish_money:
        update_stmt += f",punish_money ={punish_money}"
    if zishou:
        update_stmt += f",zishou ='{zishou}'"

    update_stmt += f" WHERE uuid ='{uuid}'"

    print(f"update_wenshu_third_money={update_stmt}")
    cursor.execute(update_stmt)
    # 提交事务
    cnx.commit()
    # 关闭游标和连接
    cursor.close()
    cnx.close()


def update_wenshu_third_money(uuid, money):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    update_stmt = f"UPDATE wenshu_third SET money ={money}, is_money = 1 WHERE uuid ={uuid}"
    print(f"update_wenshu_third_money={update_stmt}")
    cursor.execute(update_stmt)
    # 提交事务
    cnx.commit()
    # 关闭游标和连接
    cursor.close()


def query_wenshu_info_by_uuid(uuid):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    query = f"select b.case_num,b.case_num,a.content,b.full_text from wenshu_second a, wenshu b where a.uuid ='{uuid}' and a.uuid = b.uuid"
    print(f"query={query}")
    cursor.execute(query)
    rows = cursor.fetchall()
    res = []
    if rows:
        for row in rows:
            res = [row[0], row[1], row[2], row[3]]

    print(f"res={res}")
    return res


def query_wenshu_info_by_uuids(uuids):
    cnx = createMysqlConnect()
    # 创建游标对象
    cursor = cnx.cursor()
    query = (f"select b.case_num,b.case_name,b.trial,b.legal_basis,a.content ,a.uuid  "
             f"from wenshu b, wenshu_second a where b.uuid in {uuids} and a.uuid = b.uuid")

    print(f"query={query}")
    cursor.execute(query)
    rows = cursor.fetchall()
    res = []
    for row in rows:
        ll = {}
        ll.update({"案号": row[0]})
        ll.update({"案件名称": row[1]})
        ll.update({"审理程序": row[2]})
        ll.update({"法律依据": row[3]})
        ll.update({"案情摘要": json.loads(row[4])})
        ll.update({"uuid": row[5]})

        res.append(ll)
    print(f"res={res}")
    cnx.close()
    return res
