# -*- coding: utf-8 -*-
# @Time       : 2019/12/13 15:22
# @Author     : SMnRa
# @Email      : smnra@163.com
# @File       : dBConnect.py
# @Software   : PyCharm
# @description: 本脚本的作用为 创建数据库连接



import cx_Oracle as oracle

def connectOracle(userName,passWord,dataBaseIp,serviceName,dataBasePort='1521'):
    connectStatement = ""
    if userName:
        connectStatement = userName + "/"
    else:
        print("userName is Null!")
        return "userName is Null!"
    if passWord:
        connectStatement += passWord + "@"
    if dataBaseIp:
        connectStatement += dataBaseIp
    else:
        print("dataBaseIp is Null!")
        return "dataBaseIp is Null!"
    if dataBasePort:
        connectStatement += ":" + dataBasePort + "/"
    if serviceName:
        connectStatement += serviceName
    else:
        print("serviceNameis Null!")
        return "serviceNameis Null!"
    try:
        db = oracle.connect(connectStatement)
    except Exception as e:
        print(e)
        return e
    cursor = db.cursor()
    return (db,cursor)


def selectOracle(cursor,sql):
    try:
        cursor.execute(sql)
        return  cursor.fetchmany(8)
    except Exception as e:
        print(e)
        return e

def sqlOracle(cursor,sql):
    try:
        cursor.execute(sql)
        return 1
    except Exception as e:
        print(e)
        return e




def updateOrInsertOracle(cursor,sql):
    try:
        cursor.execute(sql)
        cursor.execute("commit")
        return 1
    except Exception as e:
        print(e)
        return 0


def close(db,cursor):
    cursor.execute("commit")
    cursor.close()
    db.close()


if __name__=='__main__':
    db, cursor = connectOracle('c##fast','fast*123','10.231.142.8','fast','1521')
    many_data = selectOracle(cursor, 'select *  from c_lte_custom')
    print(many_data)
    close(db, cursor)