#!/usr/bin/env python
import socket
import save_to_db
import seclog_save
import datetime
import traceback
import re

firewall_ip = "192.168.2.175" #firewall
ips_ip = "192.168.2.173"      #ips
waf_ip = "192.168.2.174"      #waf
fortM_ip = "116.228.18.37"    #Fortress machine(堡垒机)
TamP_ip = "192.168.2.178"     #Tamper protection(防篡改)

address=('',514)



def firewall(data):
    if(len(data) == 0):
        return
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logtype = "Firewall"
    msg = data
    PRI_right = data.find('>')
    PRI = data[1:PRI_right]
    PRI = int(PRI)
    level = PRI & 7
    if(level > 6):
        level = 1
    if(level>4 and level<7):
        level = 2
    if(level>2 and level<5):
        level = 3
    if(level>0 and level<3):
        level = 4
    if(level == 0):
        level = 5
    
    index = data.find('@')
    i = index
    while(i>0):
        if(data[i] == ' '):
            break
        i -= 1
    data_left = i+1
    data = data[data_left:]
    ip_list = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:\d{2,5}\b|\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", data)
    len_ip_list = len(ip_list)
    if(len_ip_list>0):
        sip = ip_list[0]
        if(":" in sip):
            index = sip.find(":")
            sport = sip[index+1:]
            sip = sip[:index]
        else:
            sport = ""    
    else:
        sip = ""
        sport = ""
        
    if(len_ip_list>1):
        dip = ip_list[1]
        if(":" in dip):
            index = dip.find(":")
            dport = dip[index+1:]
            dip = dip[:index]
        else:
            dport = "" 
    else:
        dip = ""
        dport = ""
    
    data_list = re.split(r'[ :,]+',data)
    list_l = len(data_list)
    if(list_l > 0 and data_list[0] == "Event@NET"):
        return
    if(list_l > 1 and data_list[1] == "NAT"):
        return
    eventtype = data_list[0]
    try:
        seclog_save.save_seclog(time, level, logtype, eventtype, sip, sport, dip, dport, msg)
    except:
        print(traceback.print_exc())

    try:
        save_to_db.firewall(time, level, eventtype, sip, sport, dip, dport, msg)
    except:
        print(traceback.print_exc())

def ips(data):
    PRI_right = data.find('>')
    #PRI = data[1:PRI_right]
    #PRI = int(PRI)
    #serverty = syslog_serverty[PRI]
            
    MSG_left = PRI_right + 1
    MSG = data[MSG_left:]
    MSG_list = MSG.split(';')
    time = ""
    danger_degree = 0
    breaking_sighn = 0
    event = ""
    src_addr = ""
    src_port = ""
    dst_addr = ""
    dst_port = ""
    user = ""
    smt_user = ""
    proto = ""
    for msg in MSG_list:
        index = msg.find(':')
        if(msg[:index] == "time"):
            index = index + 1
            time = msg[index :]
            if(time == None):
                time = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        if(msg[:index] == "danger_degree"):
            index = index + 1
            danger_degree = int(msg[index :])
        if(msg[:index] == "breaking_sighn"):
            index = index + 1
            breaking_sighn = int(msg[index :])
        if(msg[:index] == "event"):
            index = index + 1
            event = msg[index :]
        if(msg[:index] == "src_addr"):
            index = index + 1
            src_addr = msg[index :]
        if(msg[:index] == "src_port"):
            index = index + 1
            src_port = msg[index :]
        if(msg[:index] == "dst_addr"):
            index = index + 1
            dst_addr = msg[index :]
        if(msg[:index] == "dst_port"):
            index = index + 1
            dst_port = msg[index :]
        if(msg[:index] == "user"):
            index = index + 1
            user = msg[index :]
        if(msg[:index] == "smt_user"):
            index = index + 1
            smt_user = msg[index :]
        if(msg[:index] == "proto"):
            index = index + 1
            proto = msg[index :]
    try:
        save_to_db.ips(time, danger_degree, breaking_sighn, event, src_addr, src_port, dst_addr, dst_port, user, smt_user, proto)
    except:
        print(traceback.print_exc())
    logtype = "IPS"
    level = danger_degree
    if(level>5):
        level = 5
    eventtype = event
    sip = src_addr
    sport = src_port
    dip = dst_addr
    dport = dst_port
    msg = MSG
    try:
        seclog_save.save_seclog(time, level, logtype, eventtype, sip, sport, dip, dport, msg)
    except:
        print(traceback.print_exc())

def waf(data):
    logtype = "Waf"
    index = data.find(">") + 17
    MSG = data[index:]
    MSG_list = MSG.split(',')
    time = ""
    severity_id = 0
    msg_id = ""
    method = ""
    url = ""
    post = ""
    dip = ""
    hostname = ""
    dport = ""
    sip = ""
    sport = ""
    user_agent =""
    tag_id = ""
    action_id = ""
    response_code = ""
    matchs = ""
    rule_id = ""
    unique_id = ""
    country = ""
    province = ""
    city = ""
    for msg in MSG_list:
        index = msg.find('/')
        if("happentime" in msg[:index]):
            index = index + 1
            time = msg[index :]
            if(time == None):
                time = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        if(msg[:index] == "severity_id"):
            index = index + 1
            severity_id = int(msg[index :])
        if(msg[:index] == "msg_id"):
            index = index + 1
            msg_id = msg[index :]
        if(msg[:index] == "method"):
            index = index + 1
            method = msg[index :]
        if(msg[:index] == "url"):
            index = index + 1
            url = msg[index :]
        if(msg[:index] == "post"):
            index = index + 1
            #post = msg[index :]
        if(msg[:index] == "dip"):
            index = index + 1
            dip = msg[index :]
        if(msg[:index] == "hostname"):
            index = index + 1
            hostname = msg[index :]
        if(msg[:index] == "dport"):
            index = index + 1
            dport = msg[index :]
        if(msg[:index] == "sip"):
            index = index + 1
            sip = msg[index :]
        if(msg[:index] == "sport"):
            index = index + 1
            sport = msg[index :]
        if(msg[:index] == "user_agent"):
            index = index + 1
            user_agent = msg[index :]
        if(msg[:index] == "tag_id"):
            index = index + 1
            tag_id = msg[index :]
        if(msg[:index] == "action_id"):
            index = index + 1
            action_id = msg[index :]
        if(msg[:index] == "response_code"):
            index = index + 1
            response_code = msg[index :]
        if(msg[:index] == "match"):
            index = index + 1
            matchs = msg[index :]
        if(msg[:index] == "unique_id"):
            index = index + 1
            unique_id = msg[index :]
        if(msg[:index] == "country"):
            index = index + 1
            country = msg[index :]
        if(msg[:index] == "province"):
            index = index + 1
            province = msg[index :]
        if(msg[:index] == "city"):
            index = index + 1
            city = msg[index :]
    try:
        save_to_db.waf(time, severity_id, msg_id, method, url, post, dip,\
                                hostname, dport, sip, sport, user_agent, tag_id, action_id,\
                                response_code, matchs, rule_id, unique_id, country, province, city)

    except:
        print(traceback.print_exc())
        
    logtype = "Waf"
    level = severity_id
    if(level>5):
        level = 5
    eventtype = method
    msg = MSG
    try:
        seclog_save.save_seclog(time, level, logtype, eventtype, sip, sport, dip, dport, msg)
    except:
        print(traceback.print_exc())
    
def Tamper_protection(data):
    level_l = data.find('<') + 1
    level_r = data.find('>')
    msg_l = level_r + 1
    msg = data[msg_l:]
    data_list = re.split(r'[][]+',data)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    level = int(data[level_l:level_r])
    if(level>6):
        level = 1
    if(level==6):
        level = 2
    if(level>3 and level<6):
        level = 3
    if(level>1 and level<4):
        level = 4
    if(level<2):
        level = 5
    logtype = "Tamper protection"
    try:
        eventtype = data_list[1] + ' ' + data_list[2]
        sip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", data_list[3])
    except:
        eventtype = ""
        sip = []
    if(len(sip)>0):
        sip = sip[0]
    else:
        sip = ""
    sport = ""
    dip = ""
    dport = ""
    try:
        seclog_save.save_seclog(time, level, logtype, eventtype, sip, sport, dip, dport, msg)
    except:
        print(traceback.print_exc())

    try:
        save_to_db.Tamper_protection(time, level, eventtype, sip, sport, dip, dport, msg)
    except:
        print(traceback.print_exc())
        
def others(ip, data):
    try:
        save_to_db.others(ip, data)
    except:
        print(traceback.print_exc())
    
while (True):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind(address)
    except:
        print(traceback.print_exc())
        break
    try:
        data,addr=s.recvfrom(10240)
        if not data:
            continue
        try:
            data = data.decode()
            data = data.replace("'","")
        except:
            print(traceback.print_exc())
            continue
        addr = str(addr)
        ip = addr[2:15]  #判别日志来源
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if not p.match(ip):  #判别ip是否合法
            continue
                
        if(ip == firewall_ip):
            try:
                firewall(data)
            except:
                #print(traceback.print_exc())
                continue
                   
        elif(ip == ips_ip):
            try:
                ips(data)
            except:
                #print(traceback.print_exc())
                continue
                    
        elif(ip == waf_ip):
            try:
                waf(data)
            except:
                #print(traceback.print_exc())
                continue
            
        elif(ip == TamP_ip):
            try:
                Tamper_protection(data)
            except:
                #print(traceback.print_exc())
                continue

        else:
            try:
                others(ip, data)
            except:
                #print(traceback.print_exc())
                continue
                           
    except:
        print(traceback.print_exc())
        break
        

try:
    s.close()
except:
    print(traceback.print_exc())
