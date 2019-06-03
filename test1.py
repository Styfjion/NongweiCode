def Select1(begin, end, danger_degree):
    import pymysql
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='agr_data',
        charset="utf8")
    cur = conn.cursor()
    
    
    OutInfo = []
    sql = "select * from ips where time>%s and time<%s and danger_degree = %s" %( "'" + begin + "'","'" + end + "'",danger_degree)
    print (sql)
    cur.execute(sql)
    results = cur.fetchall()
    for r1 in results:
        print (r1[1])
        Info = []
        for r2 in r1:
            Info.append(r2)
        OutInfo.append(Info)
    #print( OutInfo )
    
    #except:
    #    print("Error: Unable to fetch data!!!")

def Select2(begin, end):
    import pymysql
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='agr_data',
        charset="utf8")
    cur = conn.cursor()
    
    
    OutInfo = []
    sql = "select t.src_addr, t.counts from (select t1.src_addr src_addr, count(*) counts from \
                                            (select * from ips where time>%s and time<%s) t1 group by src_addr) \
                                            t order by t.counts desc limit 0,10" % ("'" + begin + "'","'" + end + "'")
    print (sql)
    cur.execute(sql)
    results = cur.fetchall()
    for r1 in results:
        Info = []
        for r2 in r1:
            Info.append(r2)
        OutInfo.append(Info)
    print( OutInfo )        

begin = "2018-07-04 08:25:30"
end = "2018-07-04 09:30:30"
danger_degree = "2"
Select2(begin, end)
