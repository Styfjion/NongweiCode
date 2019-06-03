def Select0():
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
        sql = "select * from firewall"
        cur.execute(sql)
        results = cur.fetchall()
        for r1 in results:
            Info = []
            for r2 in r1:
                Info.append(r2)
            OutInfo.append(Info)
        return OutInfo
    
    except:
        print("Error: Unable to fetch data!!!")

def Select1():
    try:
        Results = Select0()
        Time = str(Results[0][0])
        print(Time)
        #print (Results[0])
    
    except:
        print("Count Error!!!")

Select1()








        
