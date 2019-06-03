import atexit
from pyVim import connect
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl
from pyVmomi import vim
import ssl
import time

import datetime
from config1 import *
from mysql_topo import *
import  os
import  detect
import socket
from config1 import *
from urllib import request,parse
url = r'https://sc.ftqq.com/SCU45342Tb4e29be9a89b07ec9e0d95dd16f42c625c74c780d63d3.send?'



oid_1 = {'S5120':['sysDescr','sysUpTime', 'sysObjectID','sysContact','sysName','1.3.6.1.4.1.25506.8.35.18.1.4','1.3.6.1.4.1.25506.8.35.18.4.3.1.6', '1.3.6.1.4.1.25506.8.35.18.1.1','1.3.6.1.4.1.25506.2.6.1.1.1.1.6.65','1.3.6.1.4.1.25506.2.6.1.1.1.1.8.65'],
         '7503E':['sysDescr','sysUpTime', 'sysObjectID','sysContact','sysName','1.3.6.1.4.1.2011.2.23.1.18.1.4','1.3.6.1.4.1.2011.2.23.1.18.4.3.1.6.1.0', '1.3.6.1.4.1.2011.2.23.1.18.1.1'],
         'Cisco':['sysDescr','sysUpTime', 'sysObjectID','sysContact','sysName']}

oid_rate = {'entCpuRate':['1.3.6.1.4.1.2011.10.2.6.1.1.1.1.6.43','1.3.6.1.4.1.2011.10.2.6.1.1.1.1.6.45','1.3.6.1.4.1.2011.10.2.6.1.1.1.1.6.47',
                          '1.3.6.1.4.1.2011.10.2.6.1.1.1.1.6.1343','1.3.6.1.4.1.2011.10.2.6.1.1.1.1.6.1345','1.3.6.1.4.1.2011.10.2.6.1.1.1.1.6.1347'],
            'entMemRate':['1.3.6.1.4.1.2011.10.2.6.1.1.1.1.8.43','1.3.6.1.4.1.2011.10.2.6.1.1.1.1.8.45','1.3.6.1.4.1.2011.10.2.6.1.1.1.1.8.47',
                          '1.3.6.1.4.1.2011.10.2.6.1.1.1.1.8.1343','1.3.6.1.4.1.2011.10.2.6.1.1.1.1.8.1345','1.3.6.1.4.1.2011.10.2.6.1.1.1.1.8.1347']}

openning_parameter = True
lastintime = time.time() - 1e3
delay_time = 90
def wechat_alarm(descript,ip,openning=False):
    global lastintime
    intime = time.time()
    if openning and int(intime-lastintime)>=delay_time:
        data = {'text': '告警信息', 'desp': '详细信息:'+descript+' ip:'+ip+' time:'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(url, data=data)
        page = request.urlopen(req).read()
        page = page.decode('utf-8')
        lastintime = intime
    else:
        pass


def switchInfo():
    info = alarm('config2.ini')
    info.cfg_load()
    alarminfo = info.cfg_dump()
    cpulevel5 = float(alarminfo['SwitchCPU']['cpulevel5'])*100
    cpulevel4 = float(alarminfo['SwitchCPU']['cpulevel4'])*100
    cpulevel3 = float(alarminfo['SwitchCPU']['cpulevel3'])*100
    memorylevel5 = float(alarminfo['SwitchMemory']['memorylevel5'])*100
    memorylevel4 = float(alarminfo['SwitchMemory']['memorylevel4'])*100
    memorylevel3 = float(alarminfo['SwitchMemory']['memorylevel3'])*100
    data = Select_topo({'type': 'switch'})
    list = []
    for i in range(len(data)):
        if 'S5120' in data[i][2]:
            oid = oid_1['S5120']
            info = alarm('config.ini')
            info.cfg_load()
            gdata = info.cfg_dump()
            community = gdata['GroupName'][data[i][1]]
            ratecpu = os.popen('snmpwalk -v 2c -c ' + community + ' ' + data[i][1] + ' ' + oid[-2]).read().split('\n')[:-1]
            T = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ip = data[i][1]
            eventtype = 'Switch'
            while '' in ratecpu:
                ratecpu.remove('')
            ratecpu = ratecpu[0].split(':')[-1].strip()
            if int(ratecpu) >= cpulevel5:
                alarmcpu = 5
                eventname = "CPU阈值告警"
                descript = "交换机CPU使用率超过%.2f%%"%cpulevel5
                detect.save_eventlog(T, ip, eventname, eventtype, alarmcpu, descript)
                data = {'text':'告警信息','desp':'详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url,data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            elif int(ratecpu) >= cpulevel4:
                alarmcpu = 4
                eventname = "CPU阈值告警"
                descript = "交换机CPU使用率超过%.2f%%" % cpulevel4
                detect.save_eventlog(T, ip, eventname, eventtype, alarmcpu, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            elif int(ratecpu) >= cpulevel3:
                alarmcpu = 3
                eventname = "CPU阈值告警"
                descript = "交换机CPU使用率超过%.2f%%" % cpulevel3
                detect.save_eventlog(T, ip, eventname, eventtype, alarmcpu, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            ratemem = os.popen('snmpwalk -v 2c -c ' + community + ' ' + data[i][1] + ' ' + oid[-1]).read().split( '\n')[:-1]
            while '' in ratemem:
                ratemem.remove('')
            ratemem = ratemem[0].split(':')[-1].strip()
            if int(ratemem) >= memorylevel5:
                alarmmem = 5
                eventname = "内存阈值告警"
                descript = "交换机内存使用率超过%.2f%%" % memorylevel5
                detect.save_eventlog(T, ip, eventname, eventtype, alarmmem, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            elif int(ratemem) >= memorylevel4:
                alarmmem = 4
                eventname = "内存阈值告警"
                descript = "交换机内存使用率超过%.2f%%" % memorylevel4
                detect.save_eventlog(T, ip, eventname, eventtype, alarmmem, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            elif int(ratemem) >= memorylevel3:
                alarmmem = 3
                eventname = "内存阈值告警"
                descript = "交换机内存使用率超过%.2f%%" % memorylevel3
                detect.save_eventlog(T, ip, eventname, eventtype, alarmmem, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
        elif '7503E' in data[i][2]:
            info = alarm('config.ini')
            info.cfg_load()
            gdata = info.cfg_dump()
            community = gdata['GroupName'][data[i][1]]
            ratelist = []
            T = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ip = data[i][1]
            eventtype = 'Switch'
            for keys, item in oid_rate.items():
                sum = 0
                for oid_value in item:
                    rate_raw = os.popen(
                        'snmpwalk -v 2c -c ' + community + ' ' + data[i][1] + ' ' + oid_value).read().split('\n')[
                               :-1]
                    while '' in rate_raw:
                        rate_raw.remove('')
                    rate_raw = rate_raw[0].split(':')[-1].strip()
                    sum += int(rate_raw)
                sum /= len(item)
                ratelist.append('%.2f' % sum)
            if float(ratelist[0]) >= cpulevel5:
                alarmcpu = 5
                eventname = "CPU阈值告警"
                descript = "交换机CPU使用率超过%.2f%%" % cpulevel5
                detect.save_eventlog(T, ip, eventname, eventtype, alarmcpu, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            elif float(ratelist[0]) >= cpulevel4:
                alarmcpu = 4
                eventname = "CPU阈值告警"
                descript = "交换机CPU使用率超过%.2f%%" % cpulevel4
                detect.save_eventlog(T, ip, eventname, eventtype, alarmcpu, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            elif float(ratelist[0]) >= cpulevel3:
                alarmcpu = 3
                eventname = "CPU阈值告警"
                descript = "交换机CPU使用率超过%.2f%%" % cpulevel3
                detect.save_eventlog(T, ip, eventname, eventtype, alarmcpu, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            if float(ratelist[1]) >= memorylevel5:
                alarmmem = 5
                eventname = "内存阈值告警"
                descript = "交换机内存使用率超过%.2f%%" % memorylevel5
                detect.save_eventlog(T, ip, eventname, eventtype, alarmmem, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            elif float(ratelist[1]) >= memorylevel4:
                alarmmem = 4
                eventname = "内存阈值告警"
                descript = "交换机内存使用率超过%.2f%%" % memorylevel4
                detect.save_eventlog(T, ip, eventname, eventtype, alarmmem, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            elif float(ratelist[1]) >= memorylevel3:
                alarmmem = 3
                eventname = "内存阈值告警"
                descript = "交换机内存使用率超过%.2f%%" % memorylevel3
                detect.save_eventlog(T, ip, eventname, eventtype, alarmmem, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            

def getaddresslist():
    """
    getaddresslist(addr) -> IP address file

    IP address read from the file.
    :param addr: IP file
    :return: Scan ip address list, or error message.
    """
    address = []
 #   try:
    path = os.getcwd()
    filepath = path+r'\iplist.txt'
    with open(filepath, "r") as iplist:
        line = iplist.readlines()
        for item in line:
            item = item.strip("\n")
            newitem = item.split(' ')
            Newitem = (newitem[0],newitem[1],newitem[2])
            address.append(Newitem)

    return address

def eventlog(iplist):
    """
    scan() -> getaddresslist()

    getaddresslist() function returns the IP address of the list.
    :param iplist: getaddresslist() Function return value.
    :param port: Need to scan the port.
    :return: None
    """
    '''
    if not isinstance(iplist, list):
        sys.exit("Function getaddresslist() return error message: %s" % iplist)
    '''
    # start_time = time.time()
    list = []
    for addr in iplist:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        host = (addr[1],int(addr[2]))
        try:
            s.connect(host)
            descr = "服务 %s:%s 连接成功." % (host[0], host[1])
            status = 1
        except Exception as e:
            descr = "服务 %s:%s 无法连接: %s" % (host[0], host[1], e)
            status = 0
        finally:
            if host[1] == 3306:
                type = "DB_Sys"
            elif host[1] == 21:
                type = "FTP"
            elif host[1] == 80:
                type = "Web_Sys"
            elif host[1] == 1433:
                type = "DB_Sys"
            list_unit = {}
            list_unit['uptime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            T = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            list_unit['IP'] = addr[1]
            ip = addr[1]+':'+addr[2]
            list_unit['port'] = addr[2]
            list_unit['eventname'] = addr[0]
            eventname = addr[0]
            list_unit['eventtype'] = type
            eventtype = type
            list_unit['level'] = 4
            level = 4
            list_unit['description'] = descr
            descript = descr
            list_unit['status'] = status
            if status == 0:
                list.append(list_unit)
                detect.save_eventlog(T, ip, eventname, eventtype, level, descript)
        s.close()

def GetVMHosts(content):
    host_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.HostSystem],
                                                        True)
    obj = [host for host in host_view.view]
    host_view.Destroy()
    return obj

def main():
    iplist = getaddresslist()
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE
    serviceInstance = SmartConnect(host='200.0.0.52',
                                   user='jiaoda',
                                   pwd='1qazXSW@',
                                   port=443,
                                   sslContext=context)
    atexit.register(Disconnect, serviceInstance)
    content = serviceInstance.RetrieveContent()

    hosts = GetVMHosts(content)
    while True:
        switchInfo()
        eventlog(iplist)
        token = -1
        for host in hosts:
            status = host.summary.overallStatus
            if status == 'red':
                T = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ip = host.summary.config.name
                eventname = "物理机故障"
                eventtype = 'Host'
                level = 5
                descript = "物理机中某些地方发生了一些故障"
                detect.save_eventlog(T, ip, eventname, eventtype, level, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            elif status == 'yellow':
                T = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ip = host.summary.config.name
                eventname = "物理机处于危险"
                eventtype = 'Host'
                level = 4
                descript = "物理机中某些地方可能发生了一些故障"
                detect.save_eventlog(T, ip, eventname, eventtype, level, descript)
                data = {'text': '告警信息', 'desp': '详细信息:'+descript+' '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(url, data=data)
                page = request.urlopen(req).read()
                page = page.decode('utf-8')
            #测试
            '''
            else:
                T = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ip = host.summary.config.name
                eventname = "物理机测试"
                eventtype = 'VM_client'
                level = 0
                descript = "物理机测试"
                detect.save_eventlog(T, ip, eventname, eventtype, level, descript)
            '''
            for vm in host.vm:
                token += 1
                vm_status = vm.summary.overallStatus
                if vm_status == 'red':
                    T = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if vm.guest.ipAddress:
                        ip = vm.guest.ipAddress
                    else:
                        ip = vm.summary.config.name
                    eventname = "虚拟机故障"
                    eventtype = 'VM_client'
                    level = 5
                    descript = "虚拟机中某些地方发生了一些故障"
                    detect.save_eventlog(T, ip, eventname, eventtype, level, descript)
                    wechat_alarm(descript,ip,openning=openning_parameter)

                elif vm_status == 'yellow':
                    T = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if vm.guest.ipAddress:
                        ip = vm.guest.ipAddress
                    else:
                        ip = vm.summary.config.name
                    eventname = "虚拟机处于危险"
                    eventtype = 'VM_client'
                    level = 4
                    descript = "虚拟机中某些地方可能发生了一些故障"
                    detect.save_eventlog(T, ip, eventname, eventtype, level, descript)
                    wechat_alarm(descript,ip,openning=openning_parameter)
                #测试
                elif token==0 or token == 1:
                    T = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if vm.guest.ipAddress:
                        ip = vm.guest.ipAddress
                    else:
                        ip = vm.summary.config.name
                    eventname = "虚拟机测试"
                    eventtype = 'VM_client'
                    level = 0
                    descript = "虚拟机测试"
                    detect.save_eventlog(T, ip, eventname, eventtype, level, descript)
                    wechat_alarm(descript,ip,openning=openning_parameter)

        info = alarm('config.ini')
        info.cfg_load()
        interval = int(info.cfg_dump('Time_interval')['interval'])
        time.sleep(interval)

if __name__ == "__main__":
    main()
exit()
