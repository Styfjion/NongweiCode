# coding=utf-8

import pymysql
import traceback
import datetime
# MySQL相关设置
mysql_host = '127.0.0.1'
mysql_user = 'root'
mysql_passwd = '1qazXSW@_xyz!'
mysql_port = '3306'
mysql_database = 'agr_data'


def my_connect():
    """链接数据库"""

    global conn, cursor

    # print MySQLdb.version_info

    
    conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, charset='utf8', autocommit=True,
                               db=mysql_database)
    
    cursor = conn.cursor()

def add_app(ID,Name,Ip,Port):
    # add
    sql = "insert into application(id,name,ip,port) values(%s,%s,%s,%s)" % (ID,"'"+ Name + "'" ,"'" + Ip + "'",Port)
    #param = (ID,Ip,Name,Type)
    my_connect()  # 打开链接
    cursor.execute(sql)
    cursor.close()
    conn.close()
        # conn.rollback()


def update_app(dictory):
    # 更新
    my_connect()
    sql = "update application set "
    flag = 0
    if "name" in dictory:
        flag = 1
        sql += "name = '%s'" %(dictory["name"])
    if "ip" in dictory:
        if flag == 1:
            sql += ",ip = '%s'" %(dictory["ip"])
        else:
            flag = 1
            sql += "ip = '%s'" %(dictory["ip"])
    if "port" in dictory:
        if flag == 1:
            sql += ",port = '%s'" %(dictory["port"])
        else:
            flag = 1
            sql += "port = '%s'" %(dictory["port"])
    sql += " where id = %d" %(dictory["id"])
        
    #sql = "update topo set ip='%s',name='%s',type='%s' where id='%d'" % (Ip,Name,Type,ID)
    try:
        cursor.execute(sql)
        cursor.close()
        conn.close()
    except:
        print(traceback.print_exc())


def Select_app(dictory):
    # 查询
    my_connect()
    if 'name' in dictory:
        if dictory['name'] == 'total':
            cursor.execute("SELECT * from application")
        else:
            cursor.execute("SELECT * from application where name ='%s'"% dictory['type'])
    elif 'ip' in dictory:
        cursor.execute("SELECT * from application where ip = '%s'" % dictory['ip'])
    elif 'port' in dictory:
        cursor.execute("SELECT * from application where port = '%s'" % dictory['port'])
    else:
        cursor.execute("SELECT * from application where id =%d" % dictory['id'])
    data = cursor.fetchall()
        #for row in data:
            # 注意int类型需要使用str函数转义
            #print('id: ', row[0], '  name: ', row[1], ' age ', row[2])
        # 提交事务
    cursor.close()  # 关闭游标
    conn.close()  # 释放数据库资源
    return data

def delete_app(ID):
    # 删除
    my_connect()
    sql = "delete from application where id='%d'" % (ID)
    # parama =(ID)
    cursor.execute(sql)
    cursor.close()
    conn.close()

def select_ip_name():
    my_connect()
    sql = "SELECT name,ip from application"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return(data)

def record_ip_health(ip,health,time,name):
    # add
    sql = "insert into iphealth(ip,health,time,name) values('%s','%s','%s','%s')" % (ip,health,time,name)
    #param = (ID,Ip,Name,Type)
    my_connect()  # 打开链接
    cursor.execute(sql)
    cursor.close()
    conn.close()
    # conn.rollback()

if __name__ == "__main__":
    data = select_ip_name()
    print(data[0])