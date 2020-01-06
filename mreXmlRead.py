# -*- coding: utf-8 -*-
# @Time       : 2020/1/6 15:50
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : mreXmlRead.py
# @Software   : PyCharm
# @description: 本脚本的作用为  解析 MRO文件








import os
import xml.etree.cElementTree as ET


def readXML(xmlFileName):
    # 读取xml文件, 并解析内容到列表
    xmlDict = {'enbId': '',
               'startTime': '',
               'endTime': '',
               'reportTime': '',
               'period': '',
               'mr': []
               }


    if os.path.exists(xmlFileName):
        tree = ET.parse(xmlFileName)
        root = tree.getroot()

        # fileHeader标签内容提取
        fileHeaderTag = root.find("fileHeader")    #查找 fileHeader 标签, 返回值为 标签属性节点的 字典
        xmlDict['startTime'] = fileHeaderTag.get('startTime','')
        xmlDict['endTime'] = fileHeaderTag.get('endTime','')
        xmlDict['reportTime'] = fileHeaderTag.get('reportTime','')
        xmlDict['period'] = fileHeaderTag.get('period','')

        # eNB 标签内容提取
        enbTag = root.find("eNB")
        xmlDict['enbId'] = enbTag.get('id','')

        # measurement 标签提取
        if enbTag :
            measurementTagList = enbTag.findall("measurement")
            xmlDict['mr'].append(measurementTagToStr(measurementTagList[0]))
            # print(xmlDict)

        print("解析完成:{}".format(xmlFileName))

    else:
        print("File Not Found!")

    return xmlDict


def measurementTagToStr(measurementTag):
    # 解析 measurement 标签信息 为 字典
    vList = []
    mrName = "MRE_15MI" # mr的类型也是表名 例如 "MRO_15MI"

    objectTagList = measurementTag.findall("object")   # 获取object 标签列表
    if objectTagList:
        for objectTag in objectTagList:
            # 遍历 object 标签
            eci = objectTag.get('id', '')
            mmeUeS1apId = objectTag.get('MmeUeS1apId', '')
            mmeGroupId = objectTag.get('MmeGroupId', '')
            mmeCode = objectTag.get('MmeCode', '')
            timeStamp = objectTag.get('TimeStamp', '')
            eventType = objectTag.get('EventType', '')

            # 获取ECI MmeUeS1apId  MmeGroupId  MmeCode  TimeStamp EventType . (xpath  /measurement/object/@id )

            vTagList = objectTag.findall('v')
            vList = vList+ [[eci,mmeUeS1apId,mmeGroupId,mmeCode,timeStamp,eventType] +
                            removeEndSpace(vTag.text," ").split(" ") for vTag in vTagList if vTagList]

    return {mrName: vList}



def removeEndSpace(str,chr):
    str = str.strip(chr)
    if str[-1] == chr:
        return removeEndSpace(str, chr)
    else:
        return str


if __name__ =="__main__":
    result = readXML('./xml/FDD-LTE_MRE_NSN_OMC_767223_20191206061500.xml')
    print(result)