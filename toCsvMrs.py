# -*- coding: utf-8 -*-
# @Time       : 2019/12/17 13:14
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : toCsvMrs.py
# @Software   : PyCharm
# @description: 本脚本的作用为  保存为csv文件



import os
from dBConnect import *
from mrsXmlRead import *
from unzipDir import *


xmlDir = './xml/'
# xml压缩包文件夹


xmlFileList = unzipDir(xmlDir,'.gz')
for xmlFile in xmlFileList:
    valueCount = 0     # 插入数据条数的计数器  超过500条 commit
    if os.path.isfile(xmlFile):
        result = readXML(xmlFile)

        if len(result.get('mr','')) > 0:
            insertSqlPart1 = "'" + result.get('enbId','') + "', " + "'" + result.get('startTime','') + "', " + "'" + result.get('endTime','') + "', " + "'" + result.get('reportTime','') + "', " + result.get('period',0) + ', '

            for mr in result['mr']:
                mrData =  list(mr.items())[0]
                csv = []
                for mdata in mrData[1]:
                    insertSqlPart2 = "'" + mdata[0] + "',"
                    insertSqlPart3 = ', '.join(mdata[1:])

                    csv.append(insertSqlPart1 + insertSqlPart2 + insertSqlPart3 + '\n')

                with open(r'./xml/{}.csv'.format(mrData[0]), 'a+', encoding=('utf-8')) as f:  # 保存本页内容到文件
                    f.writelines(csv)
                    print(r'./xml/{}.csv'.format(mrData[0]))


