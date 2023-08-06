#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   jixn_utils.py
@Time    :   2021/07/01 17:23:12
@Author  :   jixn
@Version :   1.0
'''

import time
import pyodbc
import hashlib
import yaml
import random
import os
import pymongo
import requests
from urllib import parse
import base64
from bs4 import BeautifulSoup
from pprint import pprint
import re
import sqlite3
import socket
import sys
import pika
import json
from jixn_utils import GetConfig
from pathlib import Path


# pypath = os.path.join(os.path.abspath(os.path.dirname(__file__)),"..\jixn_utils")
# sys.path.append(pypath)

class OtherTools:

    @staticmethod
    def now_time(_format="%Y-%m-%d %H:%M:%S"):
        """
        格式化返回当前时间
        :return:
        """
        format_now = time.strftime(_format, time.localtime(int(time.time())))
        return format_now

    @staticmethod  # 不强制要求实例化
    def get_ip():
        """
        :function: 获取本地ip
        :return: str
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception as e:
            print(e)
            return ''
        else:
            return ip
        finally:
            s.close()

    @staticmethod
    def run_env():
        """识别运行环境

        Returns:
            [str]: 各种环境
        """
        ip = OtherTools.get_ip()
        debugip = ["10.17.201.139"]
        testip = ["10.17.206.71"]
        formalip = ['10.17.206.97', '10.17.206.170', '10.17.206.26']
        formal_yunip = ip.startswith("10.55.")
        if ip in debugip:
            runenv = "debug"
        elif ip in testip:
            runenv = "test"
        elif ip in formalip:
            runenv = "formal"
        elif formal_yunip:
            runenv = "formal_yun"
        else:
            raise "runenv错误"
        print(f"{OtherTools.now_time()} 【当前运行环境】：{runenv}")
        return runenv


class DBTools(object):
    """这里是操作数据库的一些方法
    """

    def __init__(self, name='185') -> None:
        # f = Path(r"jixn_utils/config_db.yaml").read_text(encoding="utf-8")
        # config = yaml.safe_load(f)
        data_id = "config_db"
        group = "数据库"
        nacosconfig = GetConfig.NacosConfig("public")
        config = nacosconfig.get_yaml(data_id, group)
        self.dbconfig = config["SQL Server"][name]
        self.conn = self.open_db()
        self.cursor = self.conn.cursor()
    
    def reboot_opendb(self):
        print("重新链接数据库")
        try:
            self.dbclose()
        except:
            pass
        self.conn = self.open_db()
        self.cursor = self.conn.cursor()
        print("链接数据库成功")

    def open_db(self, driver='SQL Server'):
        """
        开启本地数据库 185,164_read,164_insert
        :param db: 数据库（默认为rreporttask）
        :return: 创建好的数据库连接
        """
        ip = OtherTools.get_ip()
        if ip in ("10.17.206.170"):
            driver = 'ODBC Driver 17 for SQL Server'
        serverName = self.dbconfig["serverName"]
        userName = self.dbconfig["userName"]
        passWord = self.dbconfig["passWord"]
        dataDase = self.dbconfig["dataDase"]
        print(f'{OtherTools.now_time()} 连接服务器{serverName} 数据库{dataDase}')
        # 建立连接并获取cursor
        conn = pyodbc.connect(driver=driver, server=serverName, user=userName, password=passWord, database=dataDase, charset="utf-8")
        return conn

    def select_one(self, sql="select ios_id from ios_main"):
        """
        查询信息
        :param time:
        :param type:
        :return:
        """
        print(OtherTools.now_time(), "正在查询数据库......")
        try:
            c = self.cursor.execute(sql)
            columns = [column[0] for column in c.description]
            result = self.cursor.fetchall()
            self.conn.commit()
            results = []
            for row in result:
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            print(OtherTools.now_time(), '查询数据失败')
            print(e)
            return ""

    def select_one_notdict(self, sql="select ios_id from ios_main"):
        """
        查询信息 不为字典模式
        :param time:
        :param type:
        :return:
        """
        print(OtherTools.now_time(), "正在查询数据库......")
        try:
            c = self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(OtherTools.now_time(), '查询数据失败')
            print(e)
            return ""

    def execute_sqls(self, sql_list):
        """
        :function: 批量执行SQL
        :param: sql_list-语句列表
        :return: boolean
        """
        try:
            for sql in sql_list:
                self.cursor.execute(sql)
        except Exception as e:
            self.conn.rollback()  # 事务回滚
            raise Exception(f'SQL执行失败 - {sql} - {e}')
        else:
            self.conn.commit()  # 事务提交
            return True

    def insert_many(self, items, table_name, num_size=500):
        """
        多条数据插入到数据库（注：插入的数据包含表里的关键字）
        :param conn:数据库
        :param items:插入的数据列表字典（列表内包含字典类型）
        :param table_name:数据库表名
        :return:无
        """
        print(OtherTools.now_time(), "更新数据表{}...".format(table_name))
        if items and len(items) > 0:

            sql1 = "insert into %s" % table_name
            sql2 = "("
            sql3 = ") values("
            sql4 = ")"
            for key in items[0].keys():  # 拼接sql语句
                sql2 += "%s," % key
                sql3 += "?,"
                # sql4 += "%s=values(%s)," % (key, key)
            sql = sql1 + sql2[:-1] + sql3[:-1] + sql4
            item_values = []
            for item in items:
                item_values.append(list(item.values()))
            num = len(item_values)
            print(OtherTools.now_time(), '一共需要处理数据%s条' % num)
            try:
                for i in range(0, num, num_size):
                    a = min(num, num_size + i)
                    self.cursor.executemany(sql, item_values[i:a])
                    self.conn.commit()
                    print(OtherTools.now_time(), "当前已经处理%s条数据" % a)
            except Exception as e:
                print(OtherTools.now_time(), '数据失败，回滚')
                print(e)
                return False
            else:
                return True
        else:
            return True

    def update_many(self, itemsz, table_name, num_size=50):
        """
        更新数据,以id为条件更新,字典第一个必须是id
        每个字典的字段名必须都存在且一样，如果某个字段为None，那么则这个字段不更新
        :param time:
        :param type:
        :return:
        """
        print(f"{OtherTools.now_time()} 共需更新数据{len(itemsz)}条")

        try:
            if itemsz and len(itemsz) > 0:
                itemsz = [itemsz[i:i + num_size] for i in range(0, len(itemsz), num_size)]
                for items in itemsz:
                    state = True
                    query_key_data = ''
                    sql1 = 'update {} set '.format(table_name)
                    sql2 = ''
                    key_list = [i for i in items[0].keys()]  # 字段列表
                    query_key = key_list[0]  # 查询的字段
                    for _, key in enumerate(key_list):
                        if _ == 0:
                            continue
                        sql_snap1 = ''
                        sql_snap = ''
                        for item in items:
                            if state:
                                query_key_data += f"'{item[query_key]}',"
                            if item[key] is None:
                                sql_snap1 += "when '{}' then {} ".format(
                                    item[query_key], key)
                            else:
                                sql_snap1 += "when '{}' then '{}' ".format(
                                    item[query_key], item[key])
                        state = False
                        sql_snap = '{} = case {} {}end, '.format(
                            key, query_key, sql_snap1)
                        sql2 += sql_snap
                    sql3 = f" where {[i for i in items[0].keys()][0]} in({query_key_data[:-1]})"
                    sql = """{}{}{}""".format(sql1, sql2[:-2], sql3)  # 生成的sql
                    # print(sql)
                    self.cursor.execute(sql)
                    self.conn.commit()
                    print(OtherTools.now_time(), "更新数据成功")
        except Exception as e:
            print(OtherTools.now_time(), '更新数据失败')
            print(e)
            return False
        else:
            return True

    def insert_update_many(self, items, table_name, only_one=["sitename", "sitesort"], updatatype=True):
        """插入更新

        Args:
            items (list): [description]
            table_name (str): [description]
            only_one (list, optional): [description]. Defaults to ["sitename", "sitesort"].
            updatatype (bool, optional): 是否更新. Defaults to True.
        """
        insert_items = []
        update_items = []
        if items and len(items) > 0:
            for item in items:

                sql = "select max(id) as ID,count(1) as num from {} where ".format(table_name)
                for i in only_one:
                    sql += " {} ='{}' and".format(i, item[i])
                # print(sql[:-3])
                sql_one = self.select_one(sql[:-3])
                if sql_one[0]["num"] == 0:
                    insert_items.append(item)
                else:
                    item0 = {}
                    item0["ID"] = sql_one[0]["ID"]
                    item0.update(item)
                    update_items.append(item0)
            ins_type = self.insert_many(insert_items, table_name)
            if updatatype:
                upd_type = self.update_many(update_items, table_name)
                if ins_type and upd_type:
                    return True
            else:
                if ins_type:
                    return True
        else:
            return True
        return False

    def dbclose(self):
        self.cursor.close()
        self.conn.close()


class DBsqlite():
    """这是一个默认创建sqlite3数据库，并包含一些基本的操作，主要可以用来做去重
    """

    def __init__(self, name='qc_db') -> None:
        self.conn = sqlite3.connect(f'{name}.db')
        self.cursor = self.conn.cursor()

    def create_db(self, table_name='qc', sql=''):
        if not sql:
            sql = f"""
            create table if not exists {table_name} 
            (id  INTEGER PRIMARY KEY autoincrement,
            info  CHAR(500)
            );
            """
        self.cursor.execute(sql)
        self.conn.commit()

    def select_one(self, sql="select info from qc"):
        """
        查询信息
        :param time:
        :param type:
        :return:
        """
        print(OtherTools.now_time(), "正在查询数据库......")
        try:
            c = self.cursor.execute(sql)
            columns = [column[0] for column in c.description]
            result = self.cursor.fetchall()
            self.conn.commit()
            results = []
            for row in result:
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            print(OtherTools.now_time(), '更新数据失败')
            print(e)
            return ""

    def is_exist(self, item, table_name='qc'):
        """判断数据是否存在

        Args:
            item (dict): 键和值 分别对应 表的字段和字段值
            table_name (str, optional): 表名. Defaults to 'qc'.

        Returns:
            int: 查询到的数量
        """
        items_list = list(item.items())
        sql0 = ''
        for items in items_list:
            sql2 = items[1] if isinstance(items[1], int) else f"'{items[1]}'"
            sql0 += f" {items[0]}={sql2} and"
        sql = f'select count(1) from {table_name} where {sql0[:-3]}'
        c = self.cursor.execute(sql)
        result = self.cursor.fetchall()[0][0]
        self.conn.commit()
        return result

    def insert_many(self, items, table_name='qc', num_size=500):
        """
        多条数据插入到数据库（注：插入的数据包含表里的关键字）
        :param conn:数据库
        :param items:插入的数据列表字典（列表内包含字典类型）
        :param table_name:数据库表名
        :return:无
        """
        print(OtherTools.now_time(), "更新数据表{}...".format(table_name))
        if items and len(items) > 0:

            sql1 = "insert into %s" % table_name
            sql2 = "("
            sql3 = ") values("
            sql4 = ")"
            for key in items[0].keys():  # 拼接sql语句
                sql2 += "%s," % key
                sql3 += "?,"
                # sql4 += "%s=values(%s)," % (key, key)
            sql = sql1 + sql2[:-1] + sql3[:-1] + sql4
            item_values = []
            for item in items:
                item_values.append(list(item.values()))
            num = len(item_values)
            print(OtherTools.now_time(), '一共需要处理数据%s条' % num)
            try:
                for i in range(0, num, num_size):
                    a = min(num, num_size + i)
                    self.cursor.executemany(sql, item_values[i:a])
                    self.conn.commit()
                    print(OtherTools.now_time(), "当前已经处理%s条数据" % a)
            except Exception as e:
                print(OtherTools.now_time(), '数据失败，回滚')
                print(e)
                return False
            else:
                return True
        else:
            return True

    def update_many(self, itemsz, table_name='qc', num_size=50):
        """
        更新数据,以id为条件更新,字典第一个必须是id
        每个字典的字段名必须都存在且一样，如果某个字段为None，那么则这个字段不更新
        :param time:
        :param type:
        :return:
        """
        print(f"{OtherTools.now_time()} 共需更新数据{len(itemsz)}条")

        try:
            if itemsz and len(itemsz) > 0:
                itemsz = [itemsz[i:i + num_size] for i in range(0, len(itemsz), num_size)]
                for items in itemsz:
                    state = True
                    query_key_data = ''
                    sql1 = 'update {} set '.format(table_name)
                    sql2 = ''
                    key_list = [i for i in items[0].keys()]  # 字段列表
                    query_key = key_list[0]  # 查询的字段
                    for _, key in enumerate(key_list):
                        if _ == 0:
                            continue
                        sql_snap1 = ''
                        sql_snap = ''
                        for item in items:
                            if state:
                                query_key_data += f"'{item[query_key]}',"
                            if item[key] is None:
                                sql_snap1 += "when '{}' then {} ".format(
                                    item[query_key], key)
                            else:
                                sql_snap1 += "when '{}' then '{}' ".format(
                                    item[query_key], item[key])
                        state = False
                        sql_snap = '{} = case {} {}end, '.format(
                            key, query_key, sql_snap1)
                        sql2 += sql_snap
                    sql3 = f" where {[i for i in items[0].keys()][0]} in({query_key_data[:-1]})"
                    sql = """{}{}{}""".format(sql1, sql2[:-2], sql3)  # 生成的sql
                    # print(sql)
                    self.cursor.execute(sql)
                    self.conn.commit()
                    print(OtherTools.now_time(), "更新数据成功")
        except Exception as e:
            print(OtherTools.now_time(), '更新数据失败')
            print(e)
            return False
        else:
            return True

    def db_close(self):
        self.conn.close()


class DwTextTools():
    """
    这里主要是处理正文的一些方法
    """

    @staticmethod
    def extract_imgurl(content, filesave):
        """这里会提取所有的img链接
        如果有base64类型的，会将其数据保存下载并在全文中直接替换为路径
        # eg: \\fileserver.finchina.local\hct\credit_test\credit\img\XZXK\2021\07\02\EBC57759-B064-F0A9-93B0-84F4EF27C6CD.jpg
        Args:
            content (str): 全文
            filesave (str): 存储路径

        Returns:
            result (list): 所有的img链接 
            content (str): 全文，如果为None，全文内容未被替换
        """
        content_type = False
        soup = BeautifulSoup(content, "html.parser")
        imglist = soup.select("img")
        result = []
        if imglist and len(imglist) > 0:
            for img_tag in imglist:
                isbase64 = False
                if 'src' not in str(img_tag).lower():
                    continue
                url = img_tag["src"]
                if url.endswith('.icon') or url.endswith('.ico') or url.endswith('.gif'):
                    continue

                if ';base64,' in url:
                    isbase64 = True
                    match = re.search(r'data:image/(\w+);', url)
                else:
                    match = re.search(r'[\s\S]*\.(\w+)$', url)
                if match:
                    suffix = match[1]
                else:
                    suffix = 'png'

                def dw_base64():
                    # 处理类型为base64的图片
                    guid = GuidTools.hash_encryto(url)
                    print(guid)
                    imgpath = os.path.join(filesave, guid + "." + suffix)
                    b64_data = url.split(';base64,')[1]
                    data = base64.b64decode(b64_data)
                    FileTools.write(data, imgpath, fs="wb")
                    return imgpath

                if isbase64:
                    imgpath = dw_base64()
                    print(img_tag, imgpath)
                    content = content.replace(str(img_tag), f"<img src='{imgpath}'/>")
                    url = imgpath
                    content_type = True
                result.append({"url": url, "isbase64": isbase64})
        if content_type:
            return result, content
        else:
            return result, None

    @staticmethod
    def extract_fileurl(content):
        """用于获取全文中的fileurl和filename

        Args:
            content ([str]): 全文

        Returns:
            [dict]: {[fileurl]:[filename]}
        """
        fileinfos = re.finditer(
            r"""(?i)<a[^<>]*?\s(href|HREF)\s*?=\s*?(\\\\|\\)?(\'|")(http[^\'"]*?)(\\\\|\\)?(\'|")[^<>]*?>([\S\s]*?)</(a|A)>""",
            content)

        # 需要去个重
        book_dict = {}
        if fileinfos:
            for fileinfo in fileinfos:  # 4  7
                fileurl1 = fileinfo.group(4)
                fileurlname1 = fileinfo.group(7)
                if fileurlname1 or fileurl1:
                    fileurlname1 = re.sub(r'<[^<>]*?>', '', fileurlname1)
                    fileurlname1 = re.sub(r'\s', '', fileurlname1)
                    fileurl1 = re.sub(r'&amp;', r'&', fileurl1)
                    fileurl1 = re.sub(r'(\s|%20)*?$', '', fileurl1)
                    if re.search(r'(?i)(htm|html|\.cn|\.cn/|\.com|\.com/)$', fileurl1):
                        continue
                    book_dict[fileurl1] = fileurlname1
        if book_dict:
            isfile = 0
            for fileurl in book_dict.keys():
                fileurlname = book_dict[fileurl]
                fileurl_1 = parse.unquote(fileurl)
                if ('\\' in fileurl_1):
                    fileurl = fileurl_1.replace('\\', '/')

                sign = re.search(
                    '(?i)(\.xls|\.xlsx|\.pdf|\.zip|\.csv|\.txt|\.rar|\.wps|\.docx|\.doc|\.gif|\.jpg|\.bmp|\.tiff|\.png|\.jpeg|\.et)',
                    fileurl)
                sign1 = re.search(
                    '(?i)(\.xls|\.xlsx|\.pdf|\.zip|\.csv|\.txt|\.rar|\.wps|\.docx|\.doc|\.gif|\.jpg|\.bmp|\.tiff|\.png|\.jpeg|\.et)',
                    fileurlname)
                if (sign or sign1):
                    isfile = 1
                    break
                else:
                    if re.search('(htm|html|\.cn|\.cn/|\.com|\.com/)$', fileurl):
                        continue
                    # 发送请求
                    headers = {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Language": "zh-CN,zh;q=0.8",
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
                    }

                    i = 1
                    while True:
                        try:
                            list_proxies = ['10.17.205.91:808', '10.17.205.96:808', '10.17.206.27:808', '']
                            proxy = random.choice(list_proxies)
                            proxies = {
                                "http": proxy,
                                "https": proxy
                            }
                            res = requests.get(
                                url=fileurl, headers=headers, proxies=proxies, timedout=60)
                        except:
                            i = i + 1
                        else:
                            break
                        if i > 3:
                            break
                    if i > 3:
                        continue
                    for key, values in res.headers.items():
                        if re.match('Content', key):
                            try:
                                file_type1 = re.search(
                                    '(?i)(\.document|/zip|/pdf|/msword|\.xls|\.xlsx|\.pdf|\.zip|\.csv|\.txt|\.rar|\.wps|\.docx|\.doc|\.gif|\.jpg|\.bmp|\.png|\.tiff|\.jpeg|\.et)(")?$',
                                    values)
                            except:
                                file_type1 = re.search(
                                    '(?i)(\.document|/zip|/pdf|/msword|\.xls|\.xlsx|\.pdf|\.zip|\.csv|\.txt|\.rar|\.wps|\.docx|\.doc|\.gif|\.jpg|\.bmp|\.png|\.tiff|\.jpeg|\.et)(")?$',
                                    values.decode('gb2312'))
                        if file_type1:
                            file_type = file_type1.group(1)
                            file_type = file_type.replace('/msword', '.doc')
                            file_type = file_type.replace('/pdf', '.pdf')
                            file_type = file_type.replace('/zip', '.zip')
                            file_type = file_type.replace('document', 'docx')
                            isfile = 1
                            break
            if isfile == 0:
                return None
            else:
                return book_dict


class RabbitMQTools():
    def __init__(self, queueName, name='test') -> None:
        f = Path(r"jixn_utils/config_db.yaml").read_text(encoding="utf-8")
        config = yaml.safe_load(f)
        self.mqconfig = config["RabbitMQ"][name]
        self.queueName = queueName
        self.hosts = self.mqconfig["hosts"]
        self.conn = self.connect_mq()

    def connect_mq(self):
        pprint(self.mqconfig)
        userinfo = pika.PlainCredentials(self.mqconfig["username"], self.mqconfig["password"])
        if len(self.hosts) == 3:
            parameters = (
                pika.ConnectionParameters(host=self.hosts[0], port=self.mqconfig["port"], connection_attempts=5,
                                          retry_delay=1, heartbeat=600, credentials=userinfo),
                pika.ConnectionParameters(host=self.hosts[1], port=self.mqconfig["port"], connection_attempts=5,
                                          retry_delay=1, heartbeat=600, credentials=userinfo),
                pika.ConnectionParameters(host=self.hosts[2], port=self.mqconfig["port"], connection_attempts=5,
                                          retry_delay=1, heartbeat=600, credentials=userinfo)
            )
        elif len(self.hosts) == 1:
            parameters = (
                pika.ConnectionParameters(host=self.hosts[0], port=self.mqconfig["port"], connection_attempts=5,
                                          retry_delay=1, heartbeat=600, credentials=userinfo))
        self.connect = pika.BlockingConnection(parameters)
        self.channel = self.connect.channel()  # 生成管道，在管道里跑不同的队列
        print(self.queueName)
        # 创建一个名为balance的队列，对queue进行durable持久化设为True(持久化第一步)
        self.balance = self.channel.queue_declare(queue=self.queueName, durable=True)  # 队列持久化
        self.channel.basic_qos(prefetch_count=1)

    def send_object(self, object, ensure_ascii=False, exchange="", priority=2):
        try:
            content = json.dumps(object, ensure_ascii=ensure_ascii)
            self.channel.basic_publish(exchange=exchange,
                                       routing_key=self.queueName,
                                       body=str(content),
                                       properties=pika.BasicProperties(delivery_mode=2,
                                                                       priority=priority))  # 设置消息持久化(持久化第二步)，将要发送的消息的属性标记为2，表示该消息要持久化,priority 优先级，越大越优先
        except Exception as e:
            print(f"{OtherTools.now_time()} 消息发送出错 {e}")
            return False
        else:
            return True

    def send_json(self, jsonStr, priority=2, exchange=""):
        try:
            self.channel.basic_publish(exchange=exchange,
                                       routing_key=self.queueName,
                                       body=str(jsonStr),
                                       properties=pika.BasicProperties(delivery_mode=2,
                                                                       priority=priority))  # 设置消息持久化(持久化第二步)，将要发送的消息的属性标记为2，表示该消息要持久化,priority 优先级，越大越优先
        except Exception as e:
            return False
        else:
            return True

    def get_one(self):
        try:
            if not self.connect or self.connect.is_closed:
                self.connect_mq()
            method_frame, header_frame, body = self.channel.basic_get(queue=self.queueName, auto_ack=False)
            if method_frame:
                return {'tag': method_frame.delivery_tag, 'body': body}
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def ack_one(self, tag):
        try:
            if not self.connect or self.connect.is_closed:
                self.connect_mq()
            self.channel.basic_ack(tag)
        except Exception as e:
            print(f'{OtherTools.now_time()} Ack Error - {e}')
            return False
        else:
            return True

    def get_mq_num(self):
        return self.balance.method.message_count

    def mqclose(self):
        print(f"{OtherTools.now_time()} 关闭mq")
        self.connect.close()


class MongodbMath():
    def __init__(self, runenv) -> None:
        # 链接数据库 qc_url（url集合） qc_domain（域名集合）
        if runenv in ["test"]:
            self.client = pymongo.MongoClient("mongodb://10.17.205.83:27017/")  # 本地mongo【可用于测试】
        elif runenv in ["formal"]:
            self.client = pymongo.MongoClient(
                "mongodb://admin:hct123.com@10.17.205.92:27000,10.17.205.92:27001,10.17.205.92:27002/")  # 本地连华为云mongo集群
        elif runenv in ["formal_yun"]:
            self.client = pymongo.MongoClient(
                "mongodb://admin:hct123.com@10.55.7.89:27000,10.55.7.91:27000,10.55.7.92:27000/")  # 华为云mongo集群
        else:
            raise "运行环境异常！"
        self.db = self.client["RepeatUrl"]
        self.url_info = self.db["qc_url"]  # qc_url qc_domain
        self.item = {}

    def whether_repeat(self, url, **kwargs):
        """
        查询库里是否重复
        允许接受多个参数，url为必要参数
        1 : 表示重复
        -1：表示不重复
        """
        ret_dict = {}

        # # 域名判断是否存在
        # item_domain = {}
        # domain_name = parse.urlparse(url).netloc # 生成域名
        # item_domain["domain_name"] = domain_name
        # _find_domain = self.url_info.find_one(item_domain)
        # if not _find_domain:
        #     ret_dict["state"] = -1
        #     ret_dict["info"] = _find_domain
        #     return ret_dict

        # url判断是否存在
        print("查询url")
        item = {}
        item["guid"] = self.get_guid(url)  # 根据url生成的guid
        for key, value in kwargs.items():
            item[key] = value
        # print(item)
        _find = self.url_info.find_one(item)
        if _find:
            ret_dict["state"] = 1
        else:
            ret_dict["state"] = -1
        ret_dict["info"] = _find
        return ret_dict

    def insert_mongo(self, url, source, html_path):
        """
        单条插入mongo
        :return: 成功插入mongo的_id
        """
        item = {}
        item["url"] = url
        item["guid"] = self.get_guid(url)  # 根据url生成的guid
        item["source"] = source  # 来源
        item["html_path"] = html_path  # html保存的公网地址
        item["update_time"] = OtherTools.now_time()  # 最新入库时间
        ins = self.url_info.insert_one(item)
        if ins:
            ret_dict = {}
            ret_dict["state"] = 1
            ret_dict["_id"] = str(ins.inserted_id)
            return ret_dict
        else:
            return {"state": -1}

    def dbcount(self):
        """
        查看当前集合的数据总数
        """
        return self.url_info.count()


class GuidTools():

    @staticmethod
    def get_guid(url):
        """通过url生成guid

        Args:
            url ([str]): 需要生成guid的url
        """
        # print(f"url: {url}")
        url = str.lower(url)
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        s1 = re.search('://([^/]*)', url)
        s8 = re.search('://([\S\s]*)', url)
        s9 = re.sub('\:\d{1,}$', '', s8[1])
        s2 = re.sub('\:\d{1,}$', '', s1[1])
        m1 = hashlib.md5()
        m1.update(s2.encode('utf-8'))
        s3 = m1.hexdigest()
        s4 = re.sub('.{22}$', '', s3)
        hash1 = hashlib.md5(s3.encode('utf-8'))
        hash1.update(s9.encode('utf-8'))
        return (str(s4) + '-' + hash1.hexdigest())

    @staticmethod
    def sixrandom():
        codeStr = "qwertyuiopasdfghjklzxcvbnm0123456789"
        codelist = list(codeStr)
        random.shuffle(codelist)
        resultlist = []
        for i in range(6):
            while True:
                s = random.choice(codelist)
                if s not in resultlist:
                    resultlist.append(s)
                    break
        random.shuffle(resultlist)
        return "".join(resultlist)

    @staticmethod
    def hashsecnew(url):
        url = str.lower(url)
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        s1 = re.search('://([^/]*)', url)
        s2 = re.sub(':\d{1,}$', '', s1[1])
        m1 = hashlib.sha1()
        m1.update(s2.encode('utf-8'))
        s3 = m1.hexdigest()
        s4 = re.sub('.{30}$', '', s3)
        hash1 = hashlib.md5(s3.encode('utf-8'))
        hash1.update(url.encode('utf-8'))
        return (str(s4) + '-' + hash1.hexdigest())

    @staticmethod
    def hashsecnew_random(url):
        url = str.lower(url)
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        s1 = re.search('://([^/]*)', url)
        s2 = re.sub(':\d{1,}$', '', s1[1])
        m1 = hashlib.sha1()
        m1.update(s2.encode('utf-8'))
        s3 = m1.hexdigest()
        s4 = re.sub('.{30}$', '', s3)
        hash1 = hashlib.md5(s3.encode('utf-8'))
        hash1.update(url.encode('utf-8'))
        return (str(s4) + '-' + hash1.hexdigest()) + '-' + OtherTools.sixrandom()

    @staticmethod
    def hash_encryto(content, method='MD5'):
        """
        :function: 对字段进行Hash加密
        :param : content-待加密内容 method-加密方法(MD5,SHA1)
        :return: str
        """
        conetent = content.encode("utf8")
        if method.lower() == 'sha1':
            hasher = hashlib.sha1(conetent)
        else:
            hasher = hashlib.md5(conetent)
        guidstr = hasher.hexdigest().upper()
        return "{}-{}-{}-{}-{}".format(guidstr[0:8], guidstr[8:12], guidstr[12:16], guidstr[16:20], guidstr[20:])


class FileTools(object):
    @staticmethod
    def create_file(filepath, encoding="utf-8"):
        try:
            file_list = os.path.split(filepath)
            filedir = file_list[0]
            if os.path.exists(filedir):
                pass
            else:
                os.makedirs(filedir)

            with open(filepath, "w+", encoding=encoding) as f:
                return True
        except:
            return False

    @staticmethod
    def read(filepath, fs="r", encoding="utf-8"):
        try:
            if "b" in fs:
                with open(filepath, fs) as f:
                    return f.read()
            else:
                with open(filepath, fs, encoding=encoding) as f:
                    return f.read()
        except:
            raise

    @staticmethod
    def readlines(filepath, fs="r", encoding="utf-8"):
        try:
            if "b" in fs:
                with open(filepath, fs) as f:
                    return f.readlines()
            else:
                with open(filepath, fs, encoding=encoding) as f:
                    return f.readlines()
        except:
            raise

    @staticmethod
    def readlines_noblank(filepath, fs="r", encoding="utf-8"):
        try:
            if "b" in fs:
                with open(filepath, fs) as f:
                    lines = f.readlines()
            else:
                with open(filepath, fs, encoding=encoding) as f:
                    lines = f.readlines()
            result = []
            for line in lines:
                result.append(line.strip())
            return result
        except:
            raise

    @staticmethod
    def write(content, filepath, fs="w", encoding="utf-8"):
        if os.path.exists(filepath):
            pass
        else:
            FileTools.create_file(filepath, encoding)
        try:
            if 'b' in fs:
                with open(filepath, fs) as f:
                    f.write(content)
            else:
                with open(filepath, fs, encoding=encoding) as f:
                    f.write(content)
            return True
        except:
            raise

    @staticmethod
    def writelines(lines, filepath, fs="w", encoding="utf-8"):
        if os.path.exists(filepath):
            pass
        else:
            FileTools.create_file(filepath, encoding)
        try:
            if 'b' in fs:
                with open(filepath, fs) as f:
                    f.writelines(lines)
            else:
                with open(filepath, fs, encoding=encoding) as f:
                    f.writelines(lines)
            return True
        except:
            raise


if __name__ == "__main__":
    # conn = open_db("185")
    html = """
    <img src="data:image/jpg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAkCAYAAABIdFAMAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAHhJREFU"/>
    <img src='http://w..asdf.png'/>
    """
    a, b = DwTextTools.cx_extract_imgurl(html, 304)
    print(a, b)
    pass
