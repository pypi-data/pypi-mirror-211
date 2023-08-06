#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   get_nacos_config.py
@Time    :   2022/03/02 13:43:34
@Author  :   jixn
@Version :   1.0
'''


import nacos
import json
import yaml
import socket


class NacosConfig(object):
    def __init__(self,NAMESPACE) -> None:
        """初始化
        Args:
            NAMESPACE (_type_): 名称空间id
        """
        self.local_ip = get_ip()
        if self.local_ip.startswith("10.17."):
            SERVER_ADDRESSES = "10.17.106.42:8848"
        elif self.local_ip.startswith("10.55."):
            SERVER_ADDRESSES = "10.55.9.179:8848"
        else:
            raise Exception("ip异常！")
        # self.client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)
        self.client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE,username='nacos',password='nacos')

    def get_yaml(self,data_id,group):
        """获取yaml类型配置

        Args:
            data_id (_type_): _description_
            group (_type_): _description_

        Returns:
            _type_: _description_
        """
        # 全局服务配置
        # data_id = "config_db"
        # group = "通用配置"
        # get config
        config = yaml.safe_load(self.client.get_config(data_id, group,timeout=5))
        return config

    def get_yaml_onip(self,data_id,group):
        """获取yaml类型配置 会默认后面加上ip 
            eg: 附件下载_10.17.201.139

        Args:
            data_id (_type_): _description_
            group (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.get_yaml(f"{data_id}_{self.local_ip}",group)

    def get_json(self,data_id,group):
        """获取yaml类型配置

        Args:
            data_id (_type_): _description_
            group (_type_): _description_

        Returns:
            _type_: _description_
        """
        config = json.loads(self.client.get_config(data_id, group,timeout=5))
        return config

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