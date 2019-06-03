
def save_vmstats(cpurate, memoryrate):
    import datetime
    import pymysql
    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='agr_data',
        charset="utf8")

    cur = conn.cursor()
    sql = "insert into vmstats(time, cpurate, memoryrate) values ('%s','%.2f','%.2f')"%(time, cpurate, memoryrate)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def read_vmstats(begin, end):
    import pymysql
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='agr_data',
        charset="utf8")
    cur = conn.cursor()
    
    try:
        OutInfo = []
        sql = "select cpurate, memoryrate from vmstats where time>%s and time<%s" %("'" + begin + "'","'" + end + "'")
        cur.execute(sql)
        results = cur.fetchall()
        for r1 in results:
            Info = []
            for r2 in r1:
                Info.append(r2)
            OutInfo.append(Info)
        print (OutInfo)
    except:
        print("Error: Unable to fetch data!!!")

cpurate = 0.8
memoryrate = 0.6
begin = "2018-06-05 10:16:25"
end = "2018-07-06 10:18:00"
save_vmstats(cpurate, memoryrate)
read_vmstats(begin, end)
