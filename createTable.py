# -*- coding: utf-8 -*-
# @Time       : 2019/12/13 16:05
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : createTable.py
# @Software   : PyCharm
# @description: 本脚本的作用为 创建数据库表结构



import os
import xml.etree.cElementTree as ET
from dBConnect import *



def readXML(xmlFileName):
    # 读取xml文件, 并解析内容到列表
    titleList = []
        #
        # {'mr': '',
        #      'title': []
        #      }
    mr = {'mr': '',
         'title': []
         }
    if os.path.exists(xmlFileName):
        tree = ET.parse(xmlFileName)
        root = tree.getroot()

        # eNB 标签内容提取
        enbTag = root.find("eNB")

        # measurement 标签提取
        if enbTag :
            measurementTagList = enbTag.findall("measurement")
            for measurementTag in measurementTagList:
                mr = {'mr': '', 'title': []}
                mr['mr'] = measurementTag.get('mrName', '').replace("MR.", "MRS_")
                values = measurementTag.find("smr").text
                values = values.strip(' ').replace('.','_')
                mr['title'] = mr['title'] + values.split(" ")
                titleList.append(mr)
                # print(mr)

        print("解析完成:{}".format(xmlFileName))

    else:
        print("File Not Found!")

    return titleList



def createTable(titleList,db,cursor):
    # 拼接 建表语句, 并执行建表语句.
    for title in titleList:
        createTableStr = "create table " + \
                         title['mr'] + \
                         "_15MI (enb_id varchar2(32), startTime varchar2(32), endTime varchar2(32), reportTime varchar2(32), period NUMBER, eci varchar2(32), " + \
                         " NUMBER, ".join(title['title']) + \
                         " NUMBER );"
        # print(title)
        print(createTableStr)
        # selectOracle(cursor, createTableStr)




if __name__ == "__main__":
    titleList = readXML('./xml/FDD-LTE_MRS_NSN_OMC_767223_20191206024500.xml')
    db, cursor = connectOracle('c##fast','fast*123','10.231.142.8','fast','1521')
    createTable(titleList, db, cursor)
    close(db, cursor)