# -*- coding: utf-8 -*-
# @Time       : 2019/12/18 11:35
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : readCsvToOracle.py
# @Software   : PyCharm
# @description: 本脚本的作用为 读取csv并入库





import os
from dBConnect import *
from mrsXmlRead import *

from multiprocessing import Process,Queue,Pipe,Pool,current_process

def getCsvFileList(dirPath,exFileName):
    dirAbsPath = os.path.abspath(dirPath)
    if os.path.isdir(dirPath):
        csvFileList = [os.path.join(dirAbsPath,csvFile) for csvFile in  os.listdir(dirPath)
                       if os.path.splitext(csvFile)[1].upper()==exFileName.upper()]
        return csvFileList
    else:
        return []


def removeEndSpace(str):
    if str[-5:-1] == "dual":
        return str
    else:
        return removeEndSpace(str[:-2])



def inOracle(csvFile):
    tableName = os.path.splitext(os.path.split(csvFile)[1])[0]
    # 从文件名提取 入库的表名

    db, cursor = connectOracle('c##fast', 'fast*123', '10.231.142.8', 'fast', '1521')
    # 连接Oracle数据库

    with open(csvFile, 'r', encoding=('utf-8')) as f:  # 保存本页内容到文件
        rows = f.readlines()


    def execSql(selectSql,i):
        selectSql = removeEndSpace(selectSql)
        # 构建插入语句
        insertSql = 'insert into {} {}'.format(tableName, selectSql)

        try:
            cursor.execute(insertSql)
            cursor.execute("commit")
            return 1
        except Exception as e:
            print(e)
            print("第{} - {} 行 入库失败!".format(i-500,i))
            return 0

        # 执行插入语句


    # 构建临时表
    selectSql = ''
    for i,row in enumerate(rows):
        selectSql += 'select {} from dual union '.format(row)
        if i%500==499 :
            execSql(selectSql,i)
            #大于1000行数据执行插入sql语句
            print(tableName, "已入库行数:",i)
            selectSql = ''
            # 将selectSql 清空

    execSql(selectSql,i)
    # 文件读完时执行插入sql语句

    close(db, cursor)
    # 关闭数据库连接
    print("已入库完成: {}, 共入库{}行.".format(tableName,i))

if __name__ == '__main__':

    csvFileList = getCsvFileList(r'./xml/','.csv')
    for csvFile in csvFileList:
        inOracle(csvFile)
