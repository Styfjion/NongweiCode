
def info(addr, data):
    import pymysql

    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='rawdata',
        charset="utf8")

    cur = conn.cursor()
    
    #print(addr, data)
    sql = "insert into data(ip, msg) values ('%s','%s')"%(addr, data)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
def otherinfo(addr, data):
    import pymysql

    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='rawdata',
        charset="utf8")

    cur = conn.cursor()
    
    #print(addr, data)
    sql = "insert into otherdata(ip, msg) values ('%s','%s')"%(addr, data)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

#addr = "1"
#data = "2"
#while(1):
#    savetomysql(addr, data)
