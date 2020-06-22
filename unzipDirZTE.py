# -*- coding: utf-8 -*-
# @Time       : 2020/6/22 12:03
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : unzipDirZTE.py
# @Software   : PyCharm
# @description: 本脚本的作用为


# -*- coding: utf-8 -*-
# @Time       : 2019/12/13 11:12
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : unzipDir.py
# @Software   : PyCharm
# @description: 本脚本的作为为 解压缩文件夹中的指定类型的压缩文件

import os
import shutil
import gzip, zipfile


def unzipDir(path, *subStrList):
    # 目录中的压缩文件解压,第一个参数为文件夹 路径,  第二个参数是 文件过滤字符串, 解压文件名中包含extName 的 文件
    dirPath = os.path.abspath(path)
    xmlFileList = []

    def unzipGzFile(gzFilePath, xmlFilePath):
        # 解压缩gz文件到 文件夹,第一个参数是gz文件名, 第二个参数是 保存 xml文件的文件夹路径

        # 创建文件夹
        xmlDirPath = os.path.split(xmlFilePath)[0]
        if not os.path.exists(xmlDirPath):
            os.makedirs(xmlDirPath)

        try:
            zipTempFile = zipfile.ZipFile(gzFilePath, 'r')
            for f_in in zipTempFile.namelist():
                xmlfileAblsPath = os.path.join(xmlDirPath, f_in)
                zipTempFile.extract(f_in, xmlfileAblsPath)
                print('解压缩：{}'.format(gzFilePath))
            return xmlfileAblsPath + '\\' + f_in
        except Exception as error:
            print(str(gzFilePath) + ' ' + str(error))
            return None
        finally:
            zipTempFile.close()

    if os.path.isdir(dirPath):
        for gzFile in os.listdir(dirPath):
            gzFileAbsPath = os.path.join(dirPath, gzFile)
            xmlFileAbsPath = gzFileAbsPath.replace('.zip', '.xml')
            if os.path.isfile(gzFileAbsPath) and fixSubName(subStrList, gzFile):
                xmlFileList.append(unzipGzFile(gzFileAbsPath, dirPath))

    return xmlFileList


def fixSubName(subStrList, Str):
    for subStr in subStrList:
        if subStr not in Str: return False
    return True


if __name__ == '__main__':
    unzipDir('./xml/ZTE/', '.zip', 'MRS')