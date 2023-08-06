#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   JudgeFile.py
@Time    :   2022/03/12 11:02:14
@Author  :   jixn
@Version :   1.0
这主要是检测附件是否是正常的
核心是去除一些可能出现的错误附件
'''

import requests
import re


class JudgeFileRight(object):
    """先判断 Content-Length 是否对的上，表示url请求完整
    对大小判断，比较小的，进行判断，大文件不进行判断
    pdf判断，通过suffix进行识别
    中间不能包括一些特殊字段，包括 <html> , 请加载JavaScript

    Args:
        object (_type_): _description_
    """
    def __init__(self,fileurl) -> None:
        self.fileurl = fileurl

    def judge_length(self):
        # 判断是否对
        hearder_len = self.headers_dict.get("Content-Length")
        if hearder_len:
            if self.res_len>=int(hearder_len):
                return True  # 正常
            else:
                return False  # 重下
        else:
            return True # 未知
    
    def judge_filesize(self):
        """判断大小是否太大，太大不检测
            1024*1024 = 1048576
        """
        if self.res_len>3000000:
            return False
        else:
            return True
    
    def file_pdf(self,text):
        if r"%%EOF" in text[-50:]:
            return True
        return False

    def file_ty(self,text):
        # 通用判断
        text = text.lower()
        if re.search(r"http://www.wj.gov.cn/index.php\?m=content&c=data&a=xxgk_down&id=\d+&catid=\d+", self.fileurl):
            return True
        elif re.search(r"http://hunan.chinatax.gov.cn/files/publicfile/ewebeditor/\d+.xls", self.fileurl):
            if r'访问被云平台拦截' in text:
                return False
            else:
                return True
        elif r'<html' in text[:300]:
            return False
        elif r'请开启javascript并刷新' in text:
            return False
        return True

    def get_rtext(self,r):
        try:
            rtext = r.text
        except Exception as e:
            print(f"r.text转换出错：{e}")
            rtext = r.content.decode("utf-8","ignore")
        return rtext


    def main(self,r,suffix):
        """主函数

        Args:
            r (_type_): response 返回信息
            suffix (_type_): 文件后缀，eg：pdf

        Returns: 是否正常
        """
        suffix = suffix.lower().replace(r".",'')
        self.res_len = len(r.content)
        self.headers_dict  = dict(r.headers) 
        # print(self.headers_dict)
        # print(self.res_len)
        if not self.judge_length():
            return False
        if self.judge_filesize():
            if suffix in ["pdf"]:
                obj = eval("self.file_"+suffix)
                rtext = self.get_rtext(r)
                text_type = obj(rtext)
            elif r"htm" in suffix: 
                print("直接是html，不判断")
                return True
            else:
                # print("通用判断")
                rtext = self.get_rtext(r)
                text_type = self.file_ty(rtext)
            return text_type
        else:
            print("太大不检测，直接认为正常")
            return True
        

if __name__=='__main__':
    r = requests.get("https://e2.sthj.sh.gov.cn:8081/xhyf/common/filedown1.do?fileId=2c361f45-f255-4bbc-8a3e-2317b428c90f")
    judge = JudgeFileRight()
    z = judge.main(r,"pdf")
    print(z)