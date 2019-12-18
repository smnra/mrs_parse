# -*- coding: utf-8 -*-
# @Time       : 2019/12/18 14:51
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : main.py
# @Software   : PyCharm
# @description: 本脚本的作用为




from toCsvMP import *
from csvToOracle import *


if __name__=='__main__':

    xmlDir = './xml/'
    # 解压缩gz压缩文件
    xmlFileList = unzipDir(xmlDir, '.gz')


    # 多线程解析xml 并保存为 csv文件
    po = Pool(5)  # 最大的进程数为5
    for xmlFile in xmlFileList:
        '''每次循环将会用空闲出来的子进程去调用目标'''
        po.apply_async(toCSV, args=(xmlFile,), callback=callback)
    print("----start----")
    po.close()  # 关闭进程池，关闭后po不再接受新的请求
    po.join()  # 等待po中的所有子进程执行完成，必须放在close语句之后
    '''如果没有添加join()，会导致有的代码没有运行就已经结束了'''
    print("-----end-----")


    # 多进程读取csv文件 并入库 oracle
    po = Pool(5)  # 最大的进程数为5
    csvFileList = getCsvFileList(r'./xml/', '.csv')
    for csvFile in csvFileList:
        # inOracle(csvFile)
        po.apply_async(inOracle, args=(csvFile,), callback=callback)
    print("----start----")
    po.close()  # 关闭进程池，关闭后po不再接受新的请求
    po.join()  # 等待po中的所有子进程执行完成，必须放在close语句之后
    '''如果没有添加join()，会导致有的代码没有运行就已经结束了'''
    print("-----end-----")