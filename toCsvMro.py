# -*- coding: utf-8 -*-
# @Time       : 2020/1/2 14:33
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : toCsvMro.py
# @Software   : PyCharm
# @description: 本脚本的作用为 MRO保存为csv文件






from mroXmlRead import *
from unzipDir import *
import time

from multiprocessing import Process,Queue,Pipe,Pool,current_process


def toCSV(xmlFile):
    start = time.time()

    valueCount = 0
    # 插入数据条数的计数器  超过500条 commit

    if os.path.isfile(xmlFile):
        result = readXML(xmlFile)

        if len(result.get('mr','')) > 0:
            mroStrPart1 = "'" + result.get('enbId','') + "', " + "'" +\
                             result.get('startTime','') + "', " + "'" + \
                             result.get('endTime','') + "', " + "'" + \
                             result.get('reportTime','') + "', " + \
                             result.get('period',0) + ', '


            for mr in result['mr']:   # 处理 result['mr']
                csv = []
                mrData =  list(mr.items())[0]
                for mdata in mrData[1]:
                    # 拼接insert 语句
                    mroStrPart2 = "'" + mdata[0] + "', "
                    mroStrPart3 = ', '.join(mdata[1:])
                    mroStr = mroStrPart1 + mroStrPart2 + mroStrPart3 + '\n'
                    csv.append(mroStr.replace("NIL","NULL"))

                with open(r'./xml/{}.csv'.format(mrData[0]), 'a+', encoding=('utf-8')) as f:  # 保存本页内容到文件
                    f.writelines(csv)
                    print(r'./xml/{}.csv'.format(mrData[0]))

            print("导出CSV文件完成:", os.path.split(xmlFile)[1], mrData[0])



            for rip in result['rip']:   # 处理 result['rip']
                csvRip = []
                ripData = list(rip.items())[0]
                for mdata in ripData[1]:
                    # 拼接insert 语句
                    mroRipStrPart2 = "'" + mdata[0] + "', "
                    mroRipStrPart3 = ', '.join(mdata[1:])
                    mroRipStr = mroStrPart1 + mroRipStrPart2 + mroRipStrPart3 + '\n'
                    csvRip.append(mroRipStr.replace("NIL", "NULL"))

                with open(r'./xml/{}.csv'.format(ripData[0]), 'a+', encoding=('utf-8')) as f:  # 保存本页内容到文件
                    f.writelines(csvRip)
                    print(r'./xml/{}.csv'.format(ripData[0]))

            print("导出CSV文件完成:", os.path.split(xmlFile)[1], ripData[0])

    print("xml文件导出完成:",str(time.time() - start))
    return str(time.time() - start)


def callback(x):
    print(' {}'.format(current_process().name,x))




if __name__ == '__main__':
    xmlDir = './xml/mro/'
    # xml压缩包文件夹
    xmlFileList = unzipDir(xmlDir, '.gz')

    po = Pool(5)  # 最大的进程数为3

    for xmlFile in xmlFileList:
        '''每次循环将会用空闲出来的子进程去调用目标'''
        # po.apply_async(toCSV, args=(xmlFile,),callback=callback)
        toCSV(xmlFile)

    print("----start----")
    po.close()  # 关闭进程池，关闭后po不再接受新的请求
    po.join()  # 等待po中的所有子进程执行完成，必须放在close语句之后
    '''如果没有添加join()，会导致有的代码没有运行就已经结束了'''
    print("-----end-----")


