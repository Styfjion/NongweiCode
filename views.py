from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.

global conn
global cur

Host = '127.0.0.1'
Passwd = '1qazXSW@_xyz!'
User = 'root'
Port = 3306
DB = 'agr_data'

def setHeader(response, http_origin):
    Origin = http_origin
    Methods = "POST, GET, PUT, DELETE, OPTIONS"
    MaxAge = "86400"
    Headers = "content-type"
    response["Access-Control-Allow-Origin"] = Origin
    response["Access-Control-Allow-Methods"] = Methods
    response["Access-Control-Max-Age"] = MaxAge
    response["Access-Control-Allow-Headers"] = Headers
    response["Access-Control-Allow-Credentials"] = "true"
    return response

def OptionsResponse(http_origin):
    if not http_origin:
        http_origin = "http://127.0.0.1:8000"
    response = HttpResponse()
    setHeader(response, http_origin)
    return response

def MyJsonResponse(data, http_origin, **kwargs):
    if not http_origin:
        http_origin = "http://127.0.0.1:8000"
    response = JsonResponse(data, json_dumps_params={'sort_keys': True}, **kwargs)
    setHeader(response, http_origin)
    return response

def connectMySQL():
    import pymysql
    global conn
    global cur
    conn = pymysql.connect(
        host=Host,
        port=Port,
        user=User,
        passwd=Passwd,
        db=DB,
        charset="utf8")
    cur = conn.cursor()

def seclog_Select0():
    global conn
    global cur
    connectMySQL()
    try:
        OutInfo = []
        sql = "select * from seclog"
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

def seclog_Select1(sql):
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
            Results = seclog_Select0()
            ret = []time, level, logtype, eventtype, sip, sport, dip, dport, msg
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

def Search_IPS_list(request):
    if request.method == 'OPTIONS':
        return OptionsResponse(request.META.get('HTTP_ORIGIN', ''))
    elif request.method == 'GET':
        try:
            Dic_para = dict(request.GET)
            sql = "select * from ips "
            flag = 0
            if("begin" in Dic_para):
                begin = Dic_para["begin"]
                if(flag == 0):
                    sql += "where time>%s" %("'" + begin + "'")
                    flag = 1
                else:
                    sql += "and time>%s" %("'" + begin + "'")

            if("end" in Dic_para):
                end = Dic_para["end"]
                if(flag == 0):
                    sql += "where time<%s" %("'" + end + "'")
                    flag = 1
                else:
                    sql += "and time<%s" %("'" + end + "'")

            if("danger_degree" in Dic_para):
                danger_degree = Dic_para["danger_degree"]
                if(flag == 0):
                    sql += "where danger_degree=%s" %("'" + danger_degree + "'")
                    flag = 1
                else:
                    sql += "and danger_degree=%s" %("'" + danger_degree + "'")

            if("breaking_sighn" in Dic_para):
                breaking_sighn = Dic_para["breaking_sighn"]
                if(flag == 0):
                    sql += "where breaking_sighn=%s" %("'" + breaking_sighn + "'")
                    flag = 1
                else:
                    sql += "and breaking_sighn=%s" %("'" + breaking_sighn + "'")

            if("event" in Dic_para):
                event = Dic_para["event"]
                if(flag == 0):
                    sql += "where event=%s" %("'" + event + "'")
                    flag = 1
                else:
                    sql += "and event=%s" %("'" + event + "'")

            if("src_addr" in Dic_para):
                src_addr = Dic_para["src_addr"]
                if(flag == 0):
                    sql += "where src_addr=%s" %("'" + src_addr + "'")
                    flag = 1
                else:
                    sql += "and src_addr=%s" %("'" + src_addr + "'")

            if("src_port" in Dic_para):
                src_port = Dic_para["src_port"]
                if(flag == 0):
                    sql += "where src_port=%s" %("'" + src_port + "'")
                    flag = 1
                else:
                    sql += "and src_port=%s" %("'" + src_port + "'")

            if("dst_addr" in Dic_para):
                dst_addr = Dic_para["dst_addr"]
                if(flag == 0):
                    sql += "where dst_addr=%s" %("'" + dst_addr + "'")
                    flag = 1
                else:
                    sql += "and dst_addr=%s" %("'" + dst_addr + "'")

            if("dst_port" in Dic_para):
                dst_port = Dic_para["dst_port"]
                if(flag == 0):
                    sql += "where dst_port=%s" %("'" + dst_port + "'")
                    flag = 1
                else:
                    sql += "and dst_port=%s" %("'" + dst_port + "'")

            if("user" in Dic_para):
                user = Dic_para["user"]
                if(flag == 0):
                    sql += "where user=%s" %("'" + user + "'")
                    flag = 1
                else:
                    sql += "and user=%s" %("'" + user + "'")

            if("smt_user" in Dic_para):
                smt_user = Dic_para["smt_user"]
                if(flag == 0):
                    sql += "where smt_user=%s" %("'" + smt_user + "'")
                    flag = 1
                else:
                    sql += "and smt_user=%s" %("'" + smt_user + "'")

            if("proto" in Dic_para):
                proto = Dic_para["proto"]
                if(flag == 0):
                    sql += "where proto=%s" %("'" + proto + "'")
                    flag = 1
                else:
                    sql += "and proto=%s" %("'" + proto + "'")

            Results = ips_Select1(sql)
            ret = []
            for i in range(len(Results)):
                Time = str(Results[i][0])
                danger_degree = Results[i][1]
                breaking_sighn = Results[i][2]
                event = Results[i][3]
                src_addr = Results[i][4]
                src_port = Results[i][5]
                dst_addr = Results[i][6]
                dst_port = Results[i][7]
                user = Results[i][8]
                smt_user = Results[i][9]
                proto = Results[i][10]
                data = {"Time":Time, "danger_degree":danger_degree, "breaking_sighn":breaking_sighn, "event":event,\
                            "src_addr":src_addr, "src_port":src_port, "dst_addr":dst_addr, "dst_port":dst_port,\
                            "user":user, "smt_user":smt_user, "proto":proto}
                ret.append(data)
            return MyJsonResponse({"IPS_list":ret}, request.META.get('HTTP_ORIGIN', ''))
        except:
            Time = "2018-07-05 11:00:00"
            danger_degree = "0"
            breaking_sighn= "1"
            event = "abcdef"
            src_addr = "196.167.9.10"
            src_port = "3306"
            dst_addr = "180.27.50.88"
            dst_port = "21"
            user = ""
            smt_user = ""
            proto = "HTTP"
            data = {"Time":Time, "danger_degree":danger_degree, "breaking_sighn":breaking_sighn, "event":event,\
                    "src_addr":src_addr, "src_port":src_port, "dst_addr":dst_addr, "dst_port":dst_port,\
                    "user":user, "smt_user":smt_user, "proto":proto}
            ret = [data]
            return MyJsonResponse({"IPS_list":ret}, request.META.get('HTTP_ORIGIN', ''))


def num_of_each_danger_degree(request):
    import pymysql
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='agr_data',
        charset="utf8")
    cur = conn.cursor()
    if request.method == 'OPTIONS':
        return OptionsResponse(request.META.get('HTTP_ORIGIN', ''))
    elif request.method == 'GET':
        try:
            begin = request.GET["begin"]
            end = request.GET["end"]
            OutInfo = []
            sql = "select t.danger_degree, t.counts from (select t1.danger_degree danger_degree, count(*) counts from \
                                        (select * from ips where time>%s and time<%s) t1 group by danger_degree) \
                                        t order by t.counts desc" % ("'" + begin + "'","'" + end + "'")
            cur.execute(sql)
            results = cur.fetchall()
            for r1 in results:
                Info = []
                for r2 in r1:
                    Info.append(r2)
                OutInfo.append(Info)
            ret = []
            for i in range(len(OutInfo)):
                danger_degree = OutInfo[i][0]
                count = OutInfo[i][1]
                data = {"danger_degree":danger_degree, "count":count}
                ret.append(data)
            return MyJsonResponse({"num_of_each_danger_degree":ret}, request.META.get('HTTP_ORIGIN', ''))
        except:
            ret = []
            danger_degree = "0"
            count = 20
            data = {"danger_degree":danger_degree, "count":count}
            ret.append(data)
            return MyJsonResponse({"num_of_each_danger_degree":ret}, request.META.get('HTTP_ORIGIN', ''))



def num_of_src_addr(request):
    import pymysql
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='agr_data',
        charset="utf8")
    cur = conn.cursor()
    if request.method == 'OPTIONS':
        return OptionsResponse(request.META.get('HTTP_ORIGIN', ''))
    elif request.method == 'GET':
        try:
            begin = request.GET["begin"]
            end = request.GET["end"]
            print (begin, end)
            OutInfo = []
            sql = "select t.src_addr, t.counts from (select t1.src_addr src_addr, count(*) counts from \
                                        (select * from ips where time>%s and time<%s) t1 group by src_addr) \
                                        t order by t.counts desc limit 0,10" % ("'" + begin + "'","'" + end + "'")
            cur.execute(sql)
            results = cur.fetchall()
            for r1 in results:
                Info = []
                for r2 in r1:
                    Info.append(r2)
                OutInfo.append(Info)
            ret = []
            for i in range(len(OutInfo)):
                src_addr = OutInfo[i][0]
                count = OutInfo[i][1]
                data = {"src_addr":src_addr, "count":count}
                ret.append(data)
	        
            return MyJsonResponse({"num_of_each_danger_degree":ret}, request.META.get('HTTP_ORIGIN', ''))
	    
        except:
            src_addr = "192.168.7.9"
            count = 20
            data = {"src_addr":src_addr, "count":count}
            ret.append(data)
            return MyJsonResponse({"num_of_each_danger_degree":ret}, request.META.get('HTTP_ORIGIN', ''))

        
