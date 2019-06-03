# coding=utf-8

import pymysql
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

    try:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, charset='utf8', autocommit=True,
                               db=mysql_database)

        print(u"\nMessage:连接MySQL成功")
    except Exception:
        print(u"\nMessage:连接失败")
        exit(20)
    cursor = conn.cursor()


def add_relation(ID1,ID2):
    
    # add
    if ID1 > ID2:
        a = ID1
        ID1 = ID2
        ID2 = a
    sql = "insert into relation(id1,id2) values (%d,%d)"%(ID1,ID2)
    print(sql)
    #param = (ID1,ID2)
    my_connect()  # 打开链接
    cursor.execute(sql)
    cursor.close()
    conn.close()
        
def Select_relation(id1 = 0,id2 = 0):
    # 查询
    my_connect()
    if id1 == 0:
        sql="SELECT * from relation"
    elif id2 == 0:
        sql="SELECT * from relation where id1=%d or id2=%d" % (id1,id1)
    else:
        sql="SELECT * from relation where id1=%d and id2=%d" % (id1,id2)
    cursor.execute(sql)
    data = cursor.fetchall()
        #for row in data:
            # 注意int类型需要使用str函数转义
            #print('id: ', row[0], '  name: ', row[1], ' age ', row[2])
        # 提交事务
    cursor.close()  # 关闭游标
    conn.close()  # 释放数据库资源
    return data


def delete_relation(ID1,ID2):
    # 删除
    my_connect()
    if ID1 > ID2:
        a = ID1
        ID1 = ID2
        ID2 = a
    sql = "delete from relation where id1=%d and id2=%d" % (ID1,ID2)
    # parama =(ID)
    cursor.execute(sql)
    cursor.close()

