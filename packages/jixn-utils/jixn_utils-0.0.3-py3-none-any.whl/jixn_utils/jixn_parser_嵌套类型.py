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

class ParserNew(object):
    def __init__(self):
        self.ret_data = {}

    def parser_one_rule(self,text,config):
        """
        处理规则，
        :param text: 需要处理的
        :param config: 配置信息，包括 rule_type,islist 和 rule
        :return: 处理后的内容，返回字符串
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

    def parser_contents(self,text,configs):
        child_rets = []
        for child_text in text:
            child_ret = {}
            for config in configs:
                child_ret[config["field"]] = self.parser_one_rule(child_text, config)
            child_rets.append(child_ret)
        return child_rets

    def parser_content(self,text,configs):
        for
        self.ret_data[config["field"]] = self.parser_one_rule(text, config)
        if "next_parser" in config:
            next_config = config["next_parser"]
            self.ret_data[next_config["field"]] = self.parser_more_rule(text, next_config)
        return self.ret_data

    def main(self,html,configs):
        for config in configs: # 规则循环
            if isinstance(html, (list,)):
                self.ret_data["listdata"] = self.parser_contents(html,config)
            else:
                self.ret_data[config["field"]] = self.parser_one_rule(html, config)
                if "next_parser" in config:
                    next_config = config["next_parser"]
                    self.ret_data[next_config["field"]] = self.parser_one_rule(text, next_config)
        return self.ret_data




def parser_one_layer(text,rules={}):
    list_datas = {
        "content": '',
        "url":"",
        "tilte":"",
        "time":''
    }
    rules = [
      {
        "field": "content",
        "rule_type": "xpath",
        "rule": "//a",
        "islist":1,
        "next_parser": [{
          "field": "content",
          "rule_type": "xpath",
          "rule": "//a"
        }]
      },
      {
        "field": "url",
        "rule_type": "xpath",
        "rule": "//a/@href"
      }
    ]
    parsernew = ParserNew()
    print(parsernew.parser_more_rule(text,rules))


    # for index,config_rule in enumerate(rules):
    #     print(config_rule)
    #     if index==0 and config_rule["field"] == 'content':
    #         _rets = parser_to_list(text,config_rule)
    #         list_datas = [{"content":conversion_type(_ret, new_type=str)} for _ret in _rets]
    #     else:
    #         for list_data in list_datas:
    #             # if config_rule["field"]
    #             _ret = conversion_type(_rets, new_type=str)
    #             list_data[config_rule["field"]] = parser_to_text(_ret,config_rule)
    #     print(list_data)
    # print(list_data)


if __name__=='__main__':
    content='''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="/css/pager.css">
<link rel="stylesheet" href="/css/bootstrap.css">
<link rel="stylesheet" href="/css/xxgkcommon.css">
<link rel="stylesheet" href="/css/publicinfo-list.css">
<link rel="stylesheet" href="/miniui/themes/default/miniui.css">
<link rel="stylesheet" href="/miniui/themes/f9/skin.css">
<link rel="stylesheet" href="/css/listSubPage.css">
<script src="/js/lib/jquery.min.js"></script>
<script src="/miniui/miniui.min.js"></script>
<script src="/js/webBuilderCommon.js"></script>
<style>
.noborder td {
	border: 0px solid #e3b788;
}
body {
	background: none;
}
body a{
    visited{color:#f00;}
}
</style>
<title>信息公开</title>

   <link rel="stylesheet" href="/css/webBuilderCommonGray.css"></head>
<body>
<div id="container">
    <div class="ewb-catalog-table">
        <div class="table-responsive">
            <table>       
                     
			                    <thead>
                                 <tr>
					                <th width="24%" style="display:table-cell;" >索引号</th>
					                <th width="24%" style="display:none;" >发文号</th>
                                    <th class="ewb-xxname" >信息名称</th>
                                    <th class="ewb-scrq">生成日期</th>
                                </tr>
                            </thead>
                        <tbody>					
						  
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202302-03814">11411023071371351L/202302-03814</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('0ed9f942-9681-462d-af1d-8c4dda52d8ec','002008');">环境简报2023年（第1期） </a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202302-03814</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>环境质量信息</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2023-02-08</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>环境简报2023年（第1期） </p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2023-02-08</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202301-03722">11411023071371351L/202301-03722</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('1d392c3e-4d0a-438b-b7b5-528a78bcd5a2','002008');">环境简报2022年（第12期）</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202301-03722</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>环境质量信息</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2023-01-10</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>环境简报2022年（第12期）</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2023-01-10</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202301-03705">11411023071371351L/202301-03705</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('de7afa20-928e-44eb-b52c-4e28d2b7c81a','002008');">水生态断面监测第12期（总第113期）</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202301-03705</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>水质环境信息</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2023-01-04</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>水生态断面监测第12期（总第113期）</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2023-01-04</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202301-03724">11411023071371351L/202301-03724</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('3cd9606e-6288-4016-b164-41e99839116a','002008');">许昌市建安区全民医疗管理有限公司许昌市建安区人民医院暨疾控中心项目环境影响评价二次公示</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202301-03724</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>建设项目环境影响评价</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2023-01-03</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>许昌市建安区全民医疗管理有限公司许昌市建安区人民医院暨疾控中心项目环境影响评价二次公示</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2023-01-03</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202212-03654">11411023071371351L/202212-03654</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('ce61bfac-c1f8-4378-93f5-ad55c52b984d','002008');">环境简报2022年（第11期）</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202212-03654</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>环境质量信息</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-12-07</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>环境简报2022年（第11期）</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-12-07</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202212-03653">11411023071371351L/202212-03653</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('16cb4108-5c3d-47d9-bac4-c0df7965e2fc','002008');">水生态断面监测第11期（总第112期）</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202212-03653</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>水质环境信息</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-12-06</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>水生态断面监测第11期（总第112期）</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-12-06</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202211-03606">11411023071371351L/202211-03606</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('0d174504-e10b-4ed0-9992-8f6056ac73e1','002008');">2022年11月25日环评文件审批公告</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202211-03606</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>建设项目环境影响评价</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-11-25</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>2022年11月25日环评文件审批公告</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-11-25</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202211-03590">11411023071371351L/202211-03590</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('c98b9d0f-8e1b-43b5-8378-5259a8188878','002008');">水生态断面监测第10期（总第111期）</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202211-03590</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>水质环境信息</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-11-17</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>水生态断面监测第10期（总第111期）</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-11-17</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202211-03589">11411023071371351L/202211-03589</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('1ce6ae16-5250-4299-9053-e46ffe103571','002008');">环境简报2022年（第10期）</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202211-03589</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>环境质量信息</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-11-17</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>环境简报2022年（第10期）</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-11-17</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202211-03606">11411023071371351L/202211-03606</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('6fde9dbc-47bb-4260-9704-9ba5ded10051','002008');">许昌宝莲沅汽车销售服务有限公司宝莲沅物流园项目全本公示</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202211-03606</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>建设项目环境影响评价</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-11-17</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>许昌宝莲沅汽车销售服务有限公司宝莲沅物流园项目全本公示</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-11-17</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202211-03606">11411023071371351L/202211-03606</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('273d13f2-61e5-43fe-bb7f-855e00508560','002008');">许昌天安清洁能源科技有限公司年洗选150万吨清洁煤生产项目环境影响报告表全本公示</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202211-03606</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>建设项目环境影响评价</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-11-17</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>许昌天安清洁能源科技有限公司年洗选150万吨清洁煤生产项目环境影响报告表全本公示</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-11-17</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202211-03606">11411023071371351L/202211-03606</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('2b281cbc-0d7e-47ee-8b06-6b9eb81bf072','002008');">河南锂尚新能源科技有限公司盐湖提锂先进设备制造项目环境影响报告表全本公示</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202211-03606</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>建设项目环境影响评价</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-11-17</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>河南锂尚新能源科技有限公司盐湖提锂先进设备制造项目环境影响报告表全本公示</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-11-17</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202211-03606">11411023071371351L/202211-03606</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('317ffad4-07c5-4311-968a-2a34dc9c805c','002008');">许昌祥迪电气科技有限公司年产300万套智能变频控制器项目环境影响报告表全本公示</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202211-03606</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>建设项目环境影响评价</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-11-17</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>许昌祥迪电气科技有限公司年产300万套智能变频控制器项目环境影响报告表全本公示</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-11-17</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202211-03606">11411023071371351L/202211-03606</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('b64a9335-0532-41ef-9615-0fb5c11d3f9a','002008');">许昌绿草地废旧物资回收有限公司年收集、贮存、转运4万吨危险废物技改项目环境影响报告表全本公示</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202211-03606</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>建设项目环境影响评价</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-11-17</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>许昌绿草地废旧物资回收有限公司年收集、贮存、转运4万吨危险废物技改项目环境影响报告表全本公示</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-11-17</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202211-03606">11411023071371351L/202211-03606</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('23f87d58-b290-4c74-940b-25ef8776c8c2','002008');">河南力鼎环保科技有限公司分散式环保设备配件生产项目环境影响报告表全本公示</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202211-03606</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>建设项目环境影响评价</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-11-17</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>河南力鼎环保科技有限公司分散式环保设备配件生产项目环境影响报告表全本公示</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-11-17</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202211-03606">11411023071371351L/202211-03606</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('cdfd55a4-db59-4e2e-b9cb-d155dc0f5015','002008');">许昌高登堡塑业有限公司年生产100万套塑料制品项目环境影响报告表全本公示</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202211-03606</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>建设项目环境影响评价</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-11-17</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>许昌高登堡塑业有限公司年生产100万套塑料制品项目环境影响报告表全本公示</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-11-17</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202211-03606">11411023071371351L/202211-03606</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('59d4ad28-b3b7-4afa-a067-e83aac697182','002008');">2022年11月17日环评文件受理公示</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202211-03606</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>建设项目环境影响评价</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-11-17</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>2022年11月17日环评文件受理公示</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-11-17</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202210-00006">11411023071371351L/202210-00006</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('a60fc92e-3212-4802-83ba-d72468928f4d','002008');">环境简报2022年（第9期）</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202210-00006</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>环境质量信息</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-10-12</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>环境简报2022年（第9期）</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-10-12</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202207-03263">11411023071371351L/202207-03263</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('99aa5aa9-2131-4568-a7cc-39f45162e8c2','002008');">公共服务事项——2022年建安区重点排污单位名录（34家）</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202207-03263</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>环境保护</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-10-10</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>公共服务事项——2022年建安区重点排污单位名录（34家）</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-10-10</span>
                                          </td>
                                      </tr>
                                
                                    <tr>
										<td width="24%" style="display:table-cell;">
                                        	<span title="11411023071371351L/202207-03260">11411023071371351L/202207-03260</span>
                                        </td>
                                        <td width="24%" style="display:none;">
                                            <span title=""></span>
                                        </td>
										   <td class="ewb-has-detail ewb-xxnr">
                                              <a class="ewb-infoname" onclick="linkToNew('0655fb29-f21c-473b-82c2-28877f12b832','002008');">其他行政职责——突发环境事件应急预案备案登记情况统计表</a>
                                              <div class="ewb-drop-detail" style="display: none; opacity: 1;">
                                                  <ul class="clearfix">
                                                      <li class="long">
                                                          <label>索 引 号 ：</label>
                                                          <p>
                                                              <b id="syh">11411023071371351L/202207-03260</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>信息分类：</label>
                                                          <p>环境保护</p>
                                                      </li>
                                                      <li>
                                                          <label>发布机构：</label>
                                                          <p>
                                                              <b>建安区政府</b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>生成日期：</label>
                                                          <p>2022-10-10</p>
                                                      </li>
                                                      <li class="long">
                                                          <label>名　称　：</label>
                                                          <p>其他行政职责——突发环境事件应急预案备案登记情况统计表</p>
                                                      </li>
                                                      <li>
                                                          <label>文　号　：</label>
                                                          <p>
                                                              <b id="docnum"></b>
                                                          </p>
                                                      </li>
                                                      <li>
                                                          <label>关 键 字 ：</label>
                                                          <p></p>
                                                      </li>
                                                  </ul>
                                              </div>
                                          </td>
                                          <td  class="ewb-rqnr">
                                              <span>2022-10-10</span>
                                          </td>
                                      </tr>
                                <tr class="noborder"><td colspan="4"><div class="pagemargin"><ul>
                                <li class="wb-page-li wb-page-item wb-page-next wb-page-family wb-page-fs12">首页</li>
                                <li class="wb-page-li wb-page-item wb-page-next wb-page-family wb-page-fs12"><上页</li>
                                <li class="wb-page-li wb-page-item current">1</li><li class="wb-page-li wb-page-item "><a href="/govxxgk/11411023071371351L/category/031/031002/031002014/031002014004/2.html">2</a> </li><li class="wb-page-li wb-page-item "><a href="/govxxgk/11411023071371351L/category/031/031002/031002014/031002014004/3.html">3</a> </li><li class="wb-page-li wb-page-item "><a href="/govxxgk/11411023071371351L/category/031/031002/031002014/031002014004/4.html">4</a> </li><li class="wb-page-li wb-page-item "><a href="/govxxgk/11411023071371351L/category/031/031002/031002014/031002014004/5.html">5</a> </li><li class="wb-page-li wb-page-item "><a href="/govxxgk/11411023071371351L/category/031/031002/031002014/031002014004/6.html">6</a> </li><li class="wb-page-li wb-page-item "><a href="/govxxgk/11411023071371351L/category/031/031002/031002014/031002014004/7.html">7</a> </li><li class="wb-page-li wb-page-item "><a href="/govxxgk/11411023071371351L/category/031/031002/031002014/031002014004/8.html">8</a> </li><li class="wb-page-li wb-page-item "><a href="/govxxgk/11411023071371351L/category/031/031002/031002014/031002014004/9.html">9</a> </li><li class="wb-page-li wb-page-item "><a href="/govxxgk/11411023071371351L/category/031/031002/031002014/031002014004/10.html">10</a> </li><li class="wb-page-li wb-page-item wb-page-next wb-page-family wb-page-fs12"><a href="/govxxgk/11411023071371351L/category/031/031002/031002014/031002014004/2.html">下页></a> </li>
                                <li class="wb-page-li wb-page-item wb-page-next wb-page-family wb-page-fs12"><a href="/govxxgk/11411023071371351L/category/031/031002/031002014/031002014004/58.html">尾页</a> </li>
                            </ul></div></td></tr><tr class="noborder"><td colspan="4"><div class="pagemargin"></div></td></tr><tr class="noborder"><td colspan="4"><div class="pagemargin"></div></td></tr></tbody>
            </table>
        </div>
    </div>

    <div class="publicinfo-pager" id="paper"></div>	
</div>
</body>
<script src="/js/xxgklist.js"></script>
</html>
'''
    rules = r"""[{"field":"content","useful":true,"rule_type":"xpath","rule":"//div[@class=\"table-responsive\"]/table/tbody/tr/td[@class=\"ewb-rqnr\"]/..","replace":null,"filter":null},{"field":"inserturl","useful":true,"rule_type":"regEx","rule":"linkToNew\\('([^']*?)'","replace":null,"filter":null},{"field":"inserturl","useful":false,"rule_type":"regEx","rule":"^([\\s\\S]*?)$","replace":"http://www.xuchang.gov.cn/openDetailDynamic.html?infoid=\\1","filter":null},{"field":"declaredate","useful":true,"rule_type":"regEx","rule":"\\s*(\\d{2,4}-\\d{1,2}-\\d{1,2})</span>","replace":null,"filter":null},{"field":"url","useful":true,"rule_type":"regEx","rule":"linkToNew\\('([^']*?)'","replace":null,"filter":null},{"field":"url","useful":false,"rule_type":"regEx","rule":"^([\\s\\S]*?)$","replace":"http://www.xuchang.gov.cn/EpointWebBuilder/zNJSAction.action?cmd=getOpenDetail&infoid=\\1&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","filter":null},{"field":"title","useful":true,"rule_type":"xpath","rule":"//a[@class=\"ewb-infoname\" ]","replace":null,"filter":null}]"""
    parser_one_layer(content,rules)
    # print(conversion_type(["asdf",'asdfsad',"dafsdf"],new_type='list_str'))
