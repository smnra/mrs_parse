# -*- coding: utf-8 -*-
# @Time    : 2019/12/13 9:25
# @Author  : SMnRa
# @Email   : smnra@163.com
# @File    : mrsXmlRead.py
# @Software: PyCharm



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
        xmlDict['startTime'] = fileHeaderTag.get('startTime','').replace("T"," ").split(".")[0]
        xmlDict['endTime'] = fileHeaderTag.get('endTime','').replace("T"," ").split(".")[0]
        xmlDict['reportTime'] = fileHeaderTag.get('reportTime','').replace("T"," ").split(".")[0]
        xmlDict['period'] = fileHeaderTag.get('period','')

        # eNB 标签内容提取
        enbTag = root.find("eNB")
        xmlDict['enbId'] = enbTag.get('id','')

        # measurement 标签提取
        if enbTag and len(xmlDict['startTime'])==19:
            measurementTagList = enbTag.findall("measurement")
            for measurementTag in measurementTagList:
                xmlDict['mr'].append(measurementTagToStr(measurementTag))
                # print(xmlDict)
        else:
            print("异常数据:{}!".format(xmlFileName))

        print("解析完成:{}".format(xmlFileName))

    else:
        print("File Not Found!")

    return xmlDict



def measurementTagToStr(measurementTag):
    # 解析 measurement 标签信息 为 字典
    vList = []
    mrName = measurementTag.get('mrName', '').replace("MR.","MRS_") + "_15MI" # mr的类型也是表名 例如 "MRS_RSRP_15MI", "MRS_RSRQ_15MI"  等

    objectTagList = measurementTag.findall("object")   # 获取object 标签列表
    if objectTagList:
        for objectTag in objectTagList:
            # 遍历 object 标签
            eci = objectTag.get('id', '')
            # 获取ECI (xpath  /measurement/object/@id )

            vTagList = objectTag.findall('v')
            vList = vList+ [[eci] + removeEndSpace(vTag.text," ").split(" ") for vTag in vTagList if vTagList]
            # MRS 数据
            # if vTagList:
            #     for vTag in vTagList:
            #         vList.append([eci] + removeEndSpace(vTag.text," ").split(" "))  # MRS 数据

    return {mrName: vList}


def removeEndSpace(str,chr):
    str = str.strip(chr)
    if str[-1] == chr:
        return removeEndSpace(str, chr)
    else:
        return str


if __name__ == "__main__":
    result = readXML('./xml/mrs/FDD-LTE_MRS_NSN_OMC_767223_20191206024500.xml')
    print(result)