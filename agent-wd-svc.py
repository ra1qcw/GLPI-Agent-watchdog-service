#-------------------------------------------------------------------------------
# Name:        GLPI-Agent-watchdog
# Purpose:
#
# Author:      ra1qcw
#
# Created:     28.09.2023
# Copyright:   (c) ra1qcw 2023
# Licence:
#-------------------------------------------------------------------------------

import time
import requests
import os
import winreg
import psutil

def getService(name):
        service = None
        try:
            service = psutil.win_service_get(name)
            service = service.as_dict()
        except Exception as ex:
            print(str(ex))
        return service

# Killing powercfg.exe
iPF = False
for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == 'powercfg.exe':
        iPF = True
if (iPF):
    time.sleep(3)
    for proc in psutil.process_iter():
        if proc.name() == 'powercfg.exe':
            proc.kill()

#Sleep before start checking
print('Start. Sleep before checking.')
for i in range(30):
    time.sleep(1)
try:
        while 1:
              wl=1
              while (wl != 0):
                wl=0

                # Killing powercfg.exe
                iPF = False
                for proc in psutil.process_iter():
                    # check whether the process name matches
                    if proc.name() == 'powercfg.exe':
                        iPF = True
                        break
                # If process found...
                if (iPF):
                    print('Waiting before killing process.')
                    time.sleep(3)
                    for proc in psutil.process_iter():
                        if proc.name() == 'powercfg.exe':
                            proc.kill()
                    print('Process kiled.')
                    continue

                access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
                try:
                    access_key = winreg.OpenKey(access_registry,r"SOFTWARE\GLPI-agent")
                except:
                    access_key = winreg.OpenKey(access_registry,r"SOFTWARE\GLPI-agent", access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY)

                glpi = winreg.QueryValueEx(access_key,"server")
                srv = glpi[0]

                if (srv.strip()==''):
                    print("No server addres. ");
                    continue
                agentPort = winreg.QueryValueEx(access_key,"httpd-port")
                agentPort = agentPort[0]
                if (agentPort.strip()==''):
                    print("No agent port. ");
                    continue

                from urllib3.exceptions import InsecureRequestWarning
                requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

                try:
                    response = requests.get('http://localhost:'+agentPort+'/status', verify=False, timeout=(3,5))
                except:
                    resAgent = -1
                else:
                    resAgent = response.status_code
                print('Agent answer: '+ ('OK' if resAgent==200 else 'Error'))

                if (resAgent == 200):
                    print('Waitng...')
                    continue

                #Sleep before second attempt
                secWait = 30
                print('Wait '+str(secWait)+' seconds.')
                for i in range(secWait):
                    time.sleep(1)


                try:
                    response = requests.get('http://localhost:'+agentPort+'/status', verify=False, timeout=(3,5))
                except:
                    resAgent = -1
                else:
                    resAgent = response.status_code
                print('Secont Agent answer: '+ ('OK' if resAgent==200 else 'Error'))
                if resAgent == 200:
                    print('Waiting...')
                    continue

                try:
                    response = requests.get(srv, verify=False, timeout=(3,5))
                except:
                    resSrv = -1
                else:
                    resSrv = response.status_code
                print('Server answer: '+'OK' if resSrv==200 else 'Error')
                if resSrv != 200:
                    continue

                os.system('net stop GLPI-agent')
                os.system('net start GLPI-agent')

                # sleep +3m after restart service
                for i in range(300):
                    time.sleep(1)

              for i in range(60):
                time.sleep(1)

except KeyboardInterrupt:
	pass
