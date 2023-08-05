# TTY system information grabber, written in Python
# Built to run on Unix-like systems, but may function on other systems
# Written and tested by Logan Allen, 2023
# PLEASE REPORT ANY ISSUES TO THE GITHUB REPOSITORY!!! www.github.com/TeaPixl
from socket import gethostname, gethostbyname
from platform import machine, system, processor, release
from datetime import datetime
import psutil
import logging
import sys
import time
import getpass
import shutil

cupImage= """                                                                                       
                                      ██    ██    ██                                    
                                    ██      ██  ██                                      
                                    ██    ██    ██                                      
                                      ██  ██      ██                                    
                                      ██    ██    ██                                    
                                                                                        
                                  ████████████████████                                  
                                  ██   ██████████   ██████                              
                                  ██                ██  ██                              
                                  ██                ██  ██                              
                                  ██                ██████                              
                                    ██            ██                                    
                                ████████████████████████                                
                                ██                    ██                                
                                  ████████████████████"""
                                     
def spinningCursor(): # shows the script is running, dosent actually mean anything :/
    while True:
        for cursor in "|/-\\":
            yield cursor

def currentUser(): #current user logged in
    user = getpass.getuser()
    print("Hello, " + user)
    
def getTime():
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("It is: "+ current_time)
    except Exception as e:
        logging.exception(e)
        print("\nSomething's wrong, Unable to display the current time")

# display the system uptime in a readable format
def bootTime():
    return time.time() - psutil.boot_time()

boot = bootTime()/60
approxBoot = round(boot, 1)

# Grab disk usage
try:
    info = []
    d = shutil.disk_usage("/") # info listed as tuple (total, used, free) *data in bytes
    info = list(d) #convert to list and remove unwanted attr.
    info.pop(2)
    total = int(info[0]) / (1024 * 1024 * 1024) # total disk space
    totalDisk = round(total, 1)
    used = int(info[1]) / (1024 * 1024 * 1024) # total used space
    usedDisk = round(used, 1)
    fraction = (usedDisk / totalDisk) *100
    newFraction = str(round(fraction, 1))
except Exception as e:
    logging.exception(e)
    print("\nSomething went wrong while trying to access your disk... Proceeding.")
    pass

# get CPU frequency
try:
    data = []
    cpuData = psutil.cpu_freq() # tuple with (current, min, max)
    data = list(cpuData)
    floatFreq = int(data[0])/1000 #convert MHz to GHz
    freq = str(round(floatFreq, 2))
except Exception as e:
    logging.exception(e)
    print("\nSomething went wrong while trying to access your CPU info.... Proceeding.")
    pass

def infoGrabber():
    try:
        data = [] # data fills this list from 0-6
        data.append(str(system())) # OS
        data.append(str(release())) # version
        data.append(str(machine())) # architecture
        data.append(str(gethostname())) # hostname, duh
        data.append(str(gethostbyname(gethostname()))) # IP addr.
        data.append(str(processor())) # CPU
        data.append(str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB") # total RAM
        usage = (psutil.virtual_memory()[2]) # RAM usage
        newUsage = str(round(usage))
        spinner = spinningCursor()
        for _ in range(7):
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
        print(cupImage)
        currentUser()
        getTime()
        print("*------------------------------*") # display the data
        print("OS: "+ data[0])
        print("VERSION: "+ data[1])
        print("CPU: "+ data[5] + " ("+ freq + " GHz)")
        print("ARCHITECTURE: "+ data[2])
        print("HOST: "+ data[3])
        print("UPTIME:", approxBoot, "minutes")
        print("IP: "+ data[4])
        print("RAM: "+ newUsage + "% used / " + data[6] + " total")
        print("DISK:", newFraction + "% used / "+ str(totalDisk) +" GB total")
        print("*------------------------------*")
    except Exception as e:
        logging.exception(e)
        print("\nSomething has failed, please check for any issues!!!")
        