import atexit
from pyVim import connect
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl
from pyVmomi import vim
import ssl
import time

import datetime
from config1 import *
from mysql_iplist2 import *
import  os
import  detect
import socket
from config1 import *
import traceback

reflect = {'green':"健康",'yellow':"危险",'red':"故障",'gray':"未知"}
def main():
    data = select_ip_name()
    namelist = [unit[0] for unit in data]
    iplist = [unit[1] for unit in data]
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE
    try:
        service_instance = SmartConnect(host='200.0.0.52',
                     user='jiaoda',
                     pwd='1qazXSW@',
                     port=443,
                     sslContext=context)
        atexit.register(connect.Disconnect, service_instance)

        content = service_instance.RetrieveContent()

        container = content.rootFolder  # starting point to look into
        viewType = [vim.VirtualMachine]  # object types to look for
        recursive = True  # whether we should look into it recursively
        containerView = content.viewManager.CreateContainerView(
            container, viewType, recursive)
        children = containerView.view
        while True:
            for vm in children:
                if vm.guest.ipAddress in iplist:
                    ip = vm.guest.ipAddress
                    if ip in iplist:
                        status = vm.summary.overallStatus
                        health = reflect[status]
                        pos = iplist.index(ip)
                        name = namelist[pos]
                        record_ip_health(ip,health,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),name)
            '''
            info = alarm('config.ini')
            info.cfg_load()
            interval = int(info.cfg_dump('Time_interval')['interval'])
            time.sleep(interval)
            '''
            time.sleep(3000)
    except:
        print(traceback.print_exc())

if __name__ == "__main__":
    main()
