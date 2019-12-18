# -*- coding: utf-8 -*-
# @Time       : 2019/12/13 11:12
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : unzipDir.py
# @Software   : PyCharm
# @description: 本脚本的作为为 解压缩文件夹中的指定类型的压缩文件

import os
import shutil
import gzip



def unzipDir(path,extName):
    # 目录中的压缩文件解压,第一个参数为文件夹 路径,  第二个参数是 文件过滤字符串, 解压文件名中包含extName 的 文件
    dirPath = os.path.abspath(path)
    xmlFileList = []
    def unzipGzFile(gzFilePath, xmlFilePath):
        # 解压缩gz文件到 文件夹,第一个参数是gz文件名, 第二个参数是 保存 xml文件的文件夹路径

        # 创建文件夹
        if not os.path.exists(os.path.split(xmlFilePath)[0]):
            os.makedirs(os.path.split(xmlFilePath)[0])

        try:
            with gzip.open(gzFilePath, 'rb') as f_in:
                with open(xmlFilePath, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    print('解压缩：{}'.format(gzFilePath))
                    return xmlFilePath
        except Exception as error:
            print(str(gzFilePath) + ' ' + str(error))
            return None


    if os.path.isdir(dirPath):
        for gzFile in os.listdir(dirPath):
            gzFileAbsPath = os.path.join(dirPath,gzFile)
            xmlFileAbsPath = gzFileAbsPath.replace('.gz','')
            if os.path.isfile(gzFileAbsPath) and extName in gzFile:
                xmlFileList.append(unzipGzFile(gzFileAbsPath,xmlFileAbsPath))

    return xmlFileList

if __name__ == '__main__':
    unzipDir('./xml/','.gz')