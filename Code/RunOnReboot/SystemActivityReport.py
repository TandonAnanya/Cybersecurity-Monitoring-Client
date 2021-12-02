import subprocess
import pandas as pd
import threading
import json
import datetime
import time

def getIOStats(final_dict):
    type_sar='-b'
    final_dict['IOStats'] = getSystemActivityReport(type_sar)

def CPUutilization(final_dict):
    type_sar='-u'
    final_dict['CPU Utilization']=getSystemActivityReport(type_sar)
    
def MemoryUtilization(final_dict):
    type_sar='-r'
    final_dict['Memory Utilization']=getSystemActivityReport(type_sar)
    
def DiskDeviceStatus(final_dict):
    type_sar='-d'
    final_dict['Disk Device Status']=getSystemActivityReport(type_sar)

def ProcessorQueue(final_dict):
    type_sar='-q'
    final_dict['Processor Queue']=getSystemActivityReport(type_sar)
    
def getSystemActivityReport(type_sar):
    command_output=subprocess.check_output(['sar', type_sar, '1', '10'])
    command_output=command_output.decode()
    command_output=command_output.split("\n")
    header=[item for item in command_output[2].strip().split(' ') if item]
    data=[item for item in command_output[13].strip().split(' ') if item]
    dict_info={}
    for i in range(1, len(data)):
        dict_info[header[i+1]]=data[i]
    return dict_info

def SystemReport():
    try:
        while True:
            stats_threads=[]
            final_dict = {}
            
            stats_threads.append(threading.Thread(target= getIOStats, args=(final_dict,)))
            stats_threads.append(threading.Thread(target= CPUutilization, args=(final_dict,)))
            stats_threads.append(threading.Thread(target= MemoryUtilization, args=(final_dict,)))
            stats_threads.append(threading.Thread(target= DiskDeviceStatus, args=(final_dict,)))
            stats_threads.append(threading.Thread(target= ProcessorQueue, args=(final_dict,)))
            
            for thread in stats_threads:
                thread.start()
            
            for thread in stats_threads:
                if thread.is_alive():
                    thread.join()
            
            
            final_dict['timestamp']=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            
            f=open('SystemActivity.json', 'w')
            json.dump(final_dict,f)
            f.close()
            final_dict = {}
    except:
        for thread in stats_threads:
            if thread.is_alive():
                thread.join()