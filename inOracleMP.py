# -*- coding: utf-8 -*-
# @Time       : 2019/12/17 11:27
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : inOracle.py
# @Software   : PyCharm
# @description: 本脚本的作用为 入库 MRS数据 到oracle中  多进程

import os
from dBConnect import *
from mrsXmlRead import *
from unzipDir import *
import time,random

from multiprocessing import Process,Queue,Pipe,Pool,current_process


def inOracle(xmlFile):
    start = time.time()
    db, cursor = connectOracle('c##fast', 'fast*123', '10.231.142.8', 'fast', '1521')
    # 连接Oracle数据库

    valueCount = 0
    # 插入数据条数的计数器  超过500条 commit

    if os.path.isfile(xmlFile):
        result = readXML(xmlFile)

        if len(result.get('mr','')) > 0:
            insertSqlPart1 = "'" + result.get('enbId','') + "', " + "'" + result.get('startTime','') + "', " + "'" + result.get('endTime','') + "', " + "'" + result.get('reportTime','') + "', " + result.get('period',0) + ', '

            for mr in result['mr']:
                mrData =  list(mr.items())[0]
                for mdata in mrData[1]:
                    # 拼接insert 语句
                    insertSqlPart2 = "'" + mdata[0] + "', "
                    insertSqlPart3 = ', '.join(mdata[1:])

                    insertSql = """insert into {} VALUES ({})""".\
                        format(mrData[0],insertSqlPart1 + insertSqlPart2 + insertSqlPart3)

                    # 执行 sql语句
                    try:
                        cursor.execute(insertSql)
                        if valueCount >= 500:
                            cursor.execute("commit")
                            valueCount = 0
                        else:
                            valueCount += 1
                    except Exception as e:
                        print(e)
                        print("入库失败:",insertSql)

                cursor.execute("commit")
                valueCount = 0
                print("入库完成:", os.path.split(xmlFile)[1], mrData[0])

    close(db, cursor)  # 关闭数据库连接
    print("入库完成:",str(time.time() - start))
    return str(time.time() - start)


def callback(x):
    print(' {}'.format(current_process().name,x))




if __name__ == '__main__':
    xmlDir = './xml/'
    # xml压缩包文件夹
    xmlFileList = unzipDir(xmlDir, '.gz')

    po = Pool(3)  # 最大的进程数为3

    for xmlFile in xmlFileList:
        '''每次循环将会用空闲出来的子进程去调用目标'''
        po.apply_async(inOracle, args=(xmlFile,),callback=callback)

    print("----start----")
    po.close()  # 关闭进程池，关闭后po不再接受新的请求
    po.join()  # 等待po中的所有子进程执行完成，必须放在close语句之后
    '''如果没有添加join()，会导致有的代码没有运行就已经结束了'''
    print("-----end-----")
