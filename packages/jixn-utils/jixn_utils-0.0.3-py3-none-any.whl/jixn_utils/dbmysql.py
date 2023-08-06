#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:吉祥鸟
# datetime:2018/10/22 14:41
# software: PyCharm
import time
from pathlib import Path
import pymysql,yaml
import warnings


warnings.filterwarnings("ignore")

"""
个人常用存储库（此库不是所有的代码都会使用）
1.获取格式化时间： ————  now_time()
2.连接本地库（默认spider）： ————  open_local_db()
3.连接线上库（默认lz_datastore）： ————  open_line_db()
4.数据库查询信息： ————  select_one()（需修改）
5.单条信息插入或更新： ————  insert_update_one()
6.多条信息插入或更新： ————  insert_update_many()
7.单条信息更新： ————  update_one()
8.单条信息插入忽略：———— insert_ignore_one()
9.多条信息插入忽略： ———— insert_ignore_many()
"""

f = Path(r"config/config_db.yaml").read_text(encoding="utf-8")
config = yaml.safe_load(f)
print(config)

def open_local_db_dict(host,user,passwd,db,port=3306,charset='utf8'):
    """
    开启本地数据库
    :param db: 数据库（默认为spider）
    :return: 创建好的数据库连接
    """
    print(now_time(), '连数据库%s' % db)
    # conn = pymysql.connect(host='bj-cynosdbmysql-grp-l2pl08mo.sql.tencentcdb.com', user='root', passwd='199618Huaihu', db=db, port=21155, charset='utf8') # 个人
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=3306, charset=charset,cursorclass=pymysql.cursors.DictCursor)
    return conn

def select_one(conn, sql="select ios_id from ios_main",close_type = True):
    """
    查询信息
    :param time:
    :param type:
    :return:
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        return result
    except Exception as e:
        print(now_time(), '查询数据失败，回滚',e)
        conn.rollback()
    if close_type:
        conn.close()


def insert_update_one(conn, item, table_name,_type=True):
    """
    单条数据插入或更新到数据库（注：插入的数据包含表里的关键字）
    :param conn:数据库
    :param item:插入的数据字典（字典类型）
    :param table_name:数据库表名
    :return:无
    """
    # print(now_time(), "更新数据表{}.....".format(table_name))
    print("item:", item)
    if item:
        cursor = conn.cursor()
        sql1 = "insert into %s" % table_name
        sql2 = "("
        sql3 = ") values("
        sql4 = ")on duplicate key update "
        for key in item.keys():  # 拼接sql语句
            sql2 += "%s," % key
            sql3 += "%s,"
            sql4 += "%s=values(%s)," % (key, key)
        try:
            item_values = list(item.values())
            item_values[1] = str(item_values[1])
            # print item_values
            sql = sql1 + sql2[:-1] + sql3[:-1] + sql4[:-1]
            # print(sql)
            cursor.execute(sql, item_values)
            conn.commit()
        except Exception as e:
            print(now_time(), '更新数据失败，回滚',e)
            conn.rollback()
            return False
        else:
            return True
    else:
        print("无数据")
        return True
    if _type:
        conn.close()
    return False

def classification_of_dict(items):
    itemsz = {}
    for item in items:
        type_str = ""
        for key in item.keys():
            type_str += key
        if type_str in itemsz:
            itemsz[type_str].append(item)
        else:
            itemsz[type_str] = [item]
    return itemsz

def ins_up_many(conn, items, table_name,_type):
    cursor = conn.cursor()
    sql1 = "insert into %s" % table_name
    sql2 = "("
    sql3 = ") values("
    sql4 = ")on duplicate key update "
    for key in items[0].keys():  # 拼接sql语句
        sql2 += "%s," % key
        sql3 += "%s,"
        sql4 += "%s=values(%s)," % (key, key)
    sql = sql1 + sql2[:-1] + sql3[:-1] + sql4[:-1]
    item_values = []
    for item in items:
        item_values.append(list(item.values()))
    num = len(item_values)
    print(now_time(), '一共需要处理数据%s条' % num)
    try:
        for i in range(0, num, 1000):
            a = min(num, 1000 + i)
            print(sql)
            cursor.executemany(sql, item_values[i:a])
            conn.commit()
            print(now_time(), "当前已经处理%s条数据" % a)
    except Exception as e:
        print(now_time(), '更新数据失败，回滚')
        print(e)
        conn.rollback()

def insert_update_many_new(conn, items, table_name,_type=True):
    print(now_time(), "更新数据表{}...".format(table_name))
    # print("item:", items)
    if items:
        itemsz = classification_of_dict(items) # 对数据进行分类
        len(itemsz)
        for items0 in itemsz.values():
            print(items0[:2])
            ins_up_many(conn, items0, table_name,_type)
    if _type:
        conn.close()


def insert_update_many(conn, items, table_name,_type=True):
    """
    多条数据插入或更新到数据库（注：插入的数据包含表里的关键字）
    :param conn:数据库
    :param items:插入的数据列表字典（列表内包含字典类型）
    :param table_name:数据库表名
    :return:无
    """
    print(now_time(), "更新数据表{}...".format(table_name))
    # print("item:", items)
    itemsz = classification_of_dict(items)
    if items:
        cursor = conn.cursor()
        sql1 = "insert into %s" % table_name
        sql2 = "("
        sql3 = ") values("
        sql4 = ")on duplicate key update "
        for key in items[0].keys():  # 拼接sql语句
            sql2 += "%s," % key
            sql3 += "%s,"
            sql4 += "%s=values(%s)," % (key, key)
        sql = sql1 + sql2[:-1] + sql3[:-1] + sql4[:-1]
        item_values = []
        for item in items:
            item_values.append(list(item.values()))
        num = len(item_values)
        print(now_time(), '一共需要处理数据%s条' % num)
        try:
            for i in range(0, num, 1000):
                a = min(num, 1000 + i)
                cursor.executemany(sql, item_values[i:a])
                conn.commit()
                print(now_time(), "当前已经处理%s条数据" % a)
        except Exception as e:
            print(now_time(), '更新数据失败，回滚')
            print(e)
            conn.rollback()
    if _type:
        conn.close()

def insert_ignore_many_new(conn, items, table_name,_type=True):
    print(now_time(), "更新数据表{}...".format(table_name))
    # print("item:", items)
    try:
        if items:
            itemsz = classification_of_dict(items) # 对数据进行分类
            len(itemsz)
            for items0 in itemsz.values():
                print(items0[:1])
                _ins_ignore_many(conn, items0, table_name,_type)
        if _type:
            conn.close()
    except Exception as e:
        print(e)
        return False
    else:
        return True

def _ins_ignore_many(conn, items, table_name,_type):
    cursor = conn.cursor()
    sql1 = "insert ignore into %s" % table_name
    sql2 = "("
    sql3 = ") values("
    sql4 = ") "
    for key in items[0].keys():  # 拼接sql语句
        sql2 += "%s," % key
        sql3 += "%s,"
        # sql4 += "%s=values(%s)," % (key, key)
    sql = sql1 + sql2[:-1] + sql3[:-1]+ sql4
    item_values = []
    for item in items:
        item_values.append(list(item.values()))
    num = len(item_values)
    print(now_time(), '一共需要处理数据%s条' % num)
    try:
        for i in range(0, num, 1000):
            a = min(num, 1000 + i)
            print(sql)
            cursor.executemany(sql, item_values[i:a])
            conn.commit()
            print(now_time(), "当前已经处理%s条数据" % a)
    except Exception as e:
        print(now_time(), '更新数据失败，回滚')
        conn.rollback()
        raise Exception(e)


def now_time(_formal = "%Y-%m-%d %H:%M:%S"):
    """
    格式化返回当前时间
    :return:
    """
    now = int(time.time())
    local_time = time.localtime(now)
    format_now = time.strftime(_formal, local_time)
    return format_now

if __name__=='__main__':
    pass