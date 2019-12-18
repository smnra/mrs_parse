# -*- coding: utf-8 -*-
# @Time       : 2019/12/17 11:27
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : inOracle.py
# @Software   : PyCharm
# @description: 本脚本的作用为 入库 MRS数据 到oracle中

import os
from dBConnect import *
from mrsXmlRead import *
from unzipDir import *


xmlDir = './xml/'
# xml压缩包文件夹

db, cursor = connectOracle('c##fast','fast*123','10.231.142.8','fast','1521')
# 连接Oracle数据库

xmlFileList = unzipDir(xmlDir,'.gz')
for xmlFile in xmlFileList:
    valueCount = 0     # 插入数据条数的计数器  超过500条 commit
    if os.path.isfile(xmlFile):
        result = readXML(xmlFile)

        if len(result.get('mr','')) > 0:
            insertSqlPart1 = "'" + result.get('enbId','') + "', " + "'" + result.get('startTime','') + "', " + "'" + result.get('endTime','') + "', " + "'" + result.get('reportTime','') + "', " + result.get('period',0) + ', '

            for mr in result['mr']:
                mrData =  list(mr.items())[0]
                for mdata in mrData[1]:
                    insertSqlPart2 = "'" + mdata[0] + "', "
                    insertSqlPart3 = ', '.join(mdata[1:])

                    insertSql = """insert into {} VALUES ({})""".\
                        format(mrData[0],insertSqlPart1 + insertSqlPart2 + insertSqlPart3)

                    try:
                        cursor.execute(insertSql)
                        if valueCount >= 500:
                            cursor.execute("commit")
                            valueCount = 0
                        else:
                            valueCount += 1
                    except Exception as e:
                        print(e)
                        print(insertSql)

                cursor.execute("commit")
                valueCount = 0

        cursor.execute("commit")
        valueCount = 0
close(db, cursor)  #关闭数据库连接

