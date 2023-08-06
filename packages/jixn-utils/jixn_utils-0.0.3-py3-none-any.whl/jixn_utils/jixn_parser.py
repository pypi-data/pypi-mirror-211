# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 9:59
# @Author  : XXX
# @Site    : 
# @File    : jixn_parser.py
# @Software: PyCharm 
# @Comment :
import ast
import json
import re
from pprint import pprint
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from lxml import etree

def conversion_type(text,old_type='',new_type=str):
    """
    类型转换，用于把数据的类型进行转换，方便抽取处理
    目前只是支持三种类型：字符串（str），json或者字典（dict），xpath对象（object）
    如果类型一致，则不进行转换！

    :param text: 原数据
    :param old_type: 原类型，可自动识别 [str,dict,object]
    :param new_type: 现类型 [str,dict,object]
    :return: 转换后的数据
    """
    if not old_type:
        if isinstance(text, (str,)):
            old_type = str
        elif isinstance(text, (dict,)):
            old_type = dict
        elif isinstance(text, (list,)):
            old_type = list
        else:
            old_type = object
    if old_type == new_type:
        new_text = text
    elif old_type==str and new_type==dict:
        new_text = ast.literal_eval(text)
    elif old_type==str and new_type==object:
        soup = BeautifulSoup(text, 'html5lib')
        fixed_html = soup.prettify()
        new_text = etree.HTML(str(fixed_html))
    elif old_type==dict and new_type==str:
        new_text = json.dumps(text)
    elif old_type==object and new_type==str:
        new_text = etree.tostring(text,encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
    elif old_type == object and new_type == dict:
        new_text = etree.tostring(text,encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
        new_text = ast.literal_eval(new_text)
    elif old_type == list and new_type == 'list_str':
        new_text = [ conversion_type(child_text,new_type=str) for child_text in text]
    elif old_type == list and new_type == str:
        new_text = ''
        for child_text in text:
            new_text += conversion_type(child_text, new_type=new_type)
    else:
        raise Exception("无相关类型转换！",old_type,new_type)
    return new_text

def get_dict(dict_obj,type,rule_str):
    """
    根据解析类型，处理json
    :param dict_obj:
    :param type:
    :param rule_str:
    :return:
    """
    rule_str = rule_str.replace('jixn_a',r"@")
    rule_str = rule_str.replace('jixn_b', r"#")
    if type=='key':
        if "int:" in rule_str:
            rule_obj = int(rule_str.replace("int:",""))
            dict_obj = dict_obj[rule_obj]
        else:
            dict_obj = dict_obj[rule_str]
    elif type=='index':
        dict_obj = dict_obj[int(rule_str)]
    else:
        raise Exception("无相关json类型处理方法！")
    return dict_obj


def parser_json_key(text,rule):
    """
    解析json模块，
    @ 表示 key 键名，如果是数字，可使用int：
    # 表示 index 下标
    eg: "@name@ind"
    :param dict_obj:
    :param rule:
    :return:
    """
    dict_obj = conversion_type(text,new_type=dict)
    rule_new = rule.replace(r"\@", 'jixn_a')
    rule_new = rule_new.replace(r"\#", 'jixn_b')
    for _ in range(100):
        begin_rule = re.search(r"^@([^@#]*)", rule_new)
        if begin_rule:
            rule_new = re.sub(r"^@([^@#]*)","",rule_new)
            print("key", begin_rule.group(1), rule_new)
            dict_obj = get_dict(dict_obj,"key",begin_rule.group(1))
        else:
            begin_rule = re.search(r"^#([^@#]*)", rule_new)
            if begin_rule:
                rule_new = re.sub(r"^#([^@#]*)", "", rule_new)
                print("index", begin_rule.group(1), rule_new)
                dict_obj = get_dict(dict_obj, "index", begin_rule.group(1))
            else:
                break
    return dict_obj


def parser_xpath(text,rule):
    """
    使用xpath解析数据
    :param text:
    :return:
    """
    p_text = conversion_type(text, new_type=object)
    result = p_text.xpath(rule)
    return result

def parser_regEx(text, rule):
    p_text = conversion_type(text, new_type=str)
    p = re.compile(rule)
    result = re.findall(p, str(p_text))
    return result

def if1(obj):
    if len(obj)==1:
        obj = obj[0]
    return obj

def parser_to_list(text,config):
    """
    处理列表类的解析，一般只有列表行
    :param text:
    :param config:
    :return:
    """
    rule_type = config["rule_type"]
    rule = config["rule"]
    if rule_type=='xpath':
        par_data = parser_xpath(text,rule)
    elif rule_type=='regEx':
        par_data =  parser_regEx(text,rule)
    elif rule_type=='json_key':
        par_data = parser_json_key(text,rule)
    elif rule_type=='const':
        par_data = rule
    else:
        raise Exception("规则异常，没有这类型的处理方法！")
    return par_data

class ParserNewList(object):
    """
    主要用来解析列表
    """
    def __init__(self,html):
        self.html = html
        # self.ret_data = {
        #     "public":{},
        #     "listdata":[]
        # }
        self.ret_data = {}

    def parser_rule(self,text,config):
        """
        处理规则，
        :param text: 需要处理的
        :param config: 配置信息，包括 rule_type,islist 和 rule
        :return: 处理后的内容，固定返回字符串
        """
        rule_type = config["rule_type"]
        rule = config["rule"]
        islist = config["islist"] if "islist" in config else 0
        if rule_type == 'xpath':
            par_data = parser_xpath(text, rule)
        elif rule_type == 'regEx':
            par_data = parser_regEx(text, rule)
        elif rule_type == 'json_key':
            par_data = parser_json_key(text, rule)
        elif rule_type == 'const':
            par_data = rule
        else:
            raise Exception("规则异常，没有这类型的处理方法！")
        if islist:
            if isinstance(par_data, (list,)):
                par_data = conversion_type(par_data, new_type="list_str")
                return par_data
            else:
                raise Exception("解析到的数据类型错误，不为list")
        else:
            par_data = conversion_type(par_data,new_type=str)
        return par_data


    def get_from_text(self,config):
        """
        获取content的来源数据，用来当前规则的解析
        :param config:
        :return:
        """
        if "from" in config:
            if config["from"] and config["from"]!= "html":
                text = self.ret_data[config["from"]]
            else:
                text = self.html
        else:
            text = self.html
        return text


    def main(self,configs):
        for config in configs: # 规则循环
            text = self.get_from_text(config)
            if isinstance(text, (list,)):
                self.ret_data[config["field"]] = [self.parser_rule(_text, config) for _text in text]
            else:
                self.ret_data[config["field"]] = self.parser_rule(text, config)
        return self.ret_data

def data_collation(rawurl,data_dict):
    """
    对抽取到来的字段进行整理
    :param data_dict:
    :return:
    """
    datas= []
    # len(data_dict)
    list_num = 1
    for key in data_dict:
        print(key)
        if isinstance(data_dict[key],(list,)):
            list_num = len(data_dict[key])
            break
    for i in range(list_num):
        data = {}
        for key in data_dict:
            if isinstance(data_dict[key], (list,)):
                data[key] = data_dict[key][i]
            else:
                data[key] = data_dict[key]
        if "url" in data:
            data["url"] = urljoin(rawurl,data["url"])
        datas.append(data)
    pprint(datas)
    return datas


def parser_more_layer(text,rules):
    if "layer_1" in rules:
        parsernew = ParserNewList(text)
        ret_data = parsernew.main(rules["layer_1"])
        layer_1_data = data_collation(ret_data)
    if "layer_2" in rules:
        parsernew = ParserNewList(text)
        ret_data = parsernew.main(rules["layer_2"])
        layer_2_data = data_collation(ret_data)
    if "layer_3" in rules:
        parsernew = ParserNewList(text)
        ret_data = parsernew.main(rules["layer_3"])
        layer_3_data = data_collation(ret_data)



if __name__=='__main__':
    content = ""
    rules = [
      {
        "from": "html",
        "field": "content",
        "rule_type": "xpath",
        "rule": "//a",
        "islist": 1
      },
      {
        "from": "content",
        "field": "url",
        "rule_type": "xpath",
        "rule": "//a/@href"
      },
      {
        "from": "url",
        "field": "url",
        "rule_type": "xpath",
        "rule": "//a/@href"
      }
    ]
    parsernew = ParserNewList(content)
    print(parsernew.main(rules))
    # print(conversion_type(["asdf",'asdfsad',"dafsdf"],new_type='list_str'))
