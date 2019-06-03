def seclog_Select(sql):
    global conn
    global cur
    
    connectMySQL()
    
    try:
        OutInfo = []
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
     
def seclog_list(request):
    if request.method == 'OPTIONS':
        return OptionsResponse(request.META.get('HTTP_ORIGIN', ''))
    elif request.method == 'GET':
        try:
            sql = "select * from seclog"
            Results = seclog_Select(sql)
            ret = []
            for i in range(len(Results)):
                time = str(Results[i][0])
                level = Results[i][1]
                logtype= Results[i][2]
                eventtype = Results[i][3]
                sip = Results[i][4]
                sport = Results[i][5]
                dip = Results[i][6]
                dport = Results[i][7]
                msg = Results[i][8]
                data = {"time":time, "level":level, "logtype":logtype, "eventtype":eventtype,\
                        "sip":sip, "sport":sport, "dip":dip, "dport":dport,"msg":msg}
                ret.append(data)
            return MyJsonResponse({"seclog_list":ret}, request.META.get('HTTP_ORIGIN', ''))
	    
        except:
            time = "未知"
            level = "未知"
            logtype= "未知"
            eventtype = "未知"
            sip = "0.0.0.0"
            sport = "0000"
            dip = "0.0.0.0"
            dport = "0000"
            msg = "未知"
            data = {"time":time, "level":level, "logtype":logtype, "eventtype":eventtype,\
                        "sip":sip, "sport":sport, "dip":dip, "dport":dport,"msg":msg}
            ret = [data]
            return MyJsonResponse({"seclog_list":ret}, request.META.get('HTTP_ORIGIN', ''))

#def search_seclog(request):
def num_of_each_logtype(request):
    if request.method == 'OPTIONS':
        return OptionsResponse(request.META.get('HTTP_ORIGIN', ''))
    elif request.method == 'GET':
        try:
            begin = request.GET["begin"]
            end = request.GET["end"]
            OutInfo = []
            sql = "select t.log_type, t.counts from (select t1.log_type log_type, count(*) counts from \
                                        (select * from seclog where time>'%s' and time<'%s') t1 group by log_type) \
                                        t order by t.counts desc" % (begin ,end)
            Results = seclog_Select(sql)
            for r1 in Results:
                Info = []
                for r2 in r1:
                    Info.append(r2)
                OutInfo.append(Info)
            ret = []
            for i in range(len(OutInfo)):
                log_type = OutInfo[i][0]
                count = OutInfo[i][1]
                data = {"log_type":log_type, "count":count}
                ret.append(data)
            return MyJsonResponse({"num_of_each_logtype":ret}, request.META.get('HTTP_ORIGIN', ''))
        except:
            ret = []
            log_type = "Firewall"
            count = 20
            data = {"log_type":log_type, "count":count}
            ret.append(data)
            return MyJsonResponse({"num_of_each_logtype":ret}, request.META.get('HTTP_ORIGIN', ''))
    


        
