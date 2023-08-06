# -*- coding: utf-8 -*-
# @Time    : 2023/3/21 14:58
# @Author  : XXX
# @Site    : 
# @File    : gen_guid.py
# @Software: PyCharm 
# @Comment :

import hashlib
import uuid
import re
import random
"""
guid生成 uniqueGuid生成
"""
class OhMyExtractor(object):
    @staticmethod
    def generate_guid(dup_text):
        """主函数调用，用于生成guid
        Args:
            dup_text (str): 生成guid的字符串，请保证唯一
            一般情况下，我们是使用正文url来生成guid，但是请保证唯一，如果不唯一，请酌情使用其他字段或者组合字段
        Returns:
            str: guid
        """
        dup_text = re.sub(r'\s+',"",dup_text)
        md5 = OhMyExtractor.hash_encryto(dup_text, method='MD5')
        guid = OhMyExtractor.generate_GUID(md5, traceable=True)
        return str(guid).upper()

    @staticmethod
    def generate_uniqueGuid(url):
        """主函数调用，用于生成uniqueGuid
        Args:
            url (srt): 一般是全文链接
        Returns:
            str: uniqueGuid
        """
        assert url
        return OhMyExtractor.hashsecnew(url) + '-' + OhMyExtractor.sixrandom()
    @staticmethod
    def hash_encryto(content, method='MD5'):
        """
        :function: 对字段进行Hash加密
        :param : content-待加密内容 method-加密方法(MD5,SHA1)
        :return: str
        """
        conetent = content.encode("utf8")
        if method.lower() == 'md5':
            hasher = hashlib.md5(conetent)
        elif method.lower() == 'sha1':
            hasher = hashlib.sha1(conetent)
        else:
            hasher = hashlib.md5(conetent)
        return hasher.hexdigest()
    @staticmethod
    def generate_GUID(content='', traceable=True):
        """
        :function: 对字段进行Hash加密
        :param : content-待生成内容 traceable-是否可回溯
        :return: str
        """
        if not content:
            return str(uuid.uuid1())
        else:
            if traceable:
                return str(uuid.uuid3(uuid.NAMESPACE_URL, content))
            else:
                return str(uuid.uuid1())

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