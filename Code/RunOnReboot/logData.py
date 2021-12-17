import time
import json
import requests
import datetime
import sys

def needNewToken():

    # Interval in seconds    
    # interval = 30

    interval = 30*60

    currentTime = time.time()

    try:
        tokenTimeFile = open("tokenTime.txt", "r")
    except:
        tokenTimeFile = open("tokenTime.txt", "w")
        tokenTimeFile.write(str(currentTime))
        tokenTimeFile.close()
                
    print("Current Time: ",currentTime)
    tokenTimeFile = open("tokenTime.txt", "r")
    readTime = tokenTimeFile.readline()
    tokenTimeFile.close()    
    previousTime = float(readTime)      
    print("Previous Time: ",previousTime)      

    print("Need: ",currentTime,previousTime+interval)    

    if currentTime<previousTime+interval:        
        print("False")
        return False
    
    tokenTimeFile = open("tokenTime.txt", "w")
    tokenTimeFile.write(str(currentTime))
    tokenTimeFile.close()

    print("True")
    return True

def accessNewToken():
    url = "35.235.92.92:4000"    
    channelName = "common"
    smartContractName = "digitalTwin"
    postURL = 'http://{}/users/register'.format(url)

    headers = {
        'Content-Type':'application/json',        
    }

    body = {
        "username": "user1",
        "orgName": "Manufacturer",
        "role": "manufacturer",
        "attrs": [
            {
                "name":"client1",
                "value":"yes",
                "ecert": True
            }, 
        ],
        "secret": "9198e23d54de4cc9a887d003f5872df2"
    }

    response = requests.post(postURL, data=json.dumps(body), headers=headers)
    token = response.json()['token']
    tokenFile = open('token.txt', 'w')
    tokenFile.write(token)
    tokenFile.close()
    return token

def getToken():

    if not needNewToken():
        try:            
            tokenFile = open('token.txt', 'r')            
        except:
            return accessNewToken()
        return tokenFile.readline()
    else:
        return accessNewToken()    

def createDigitalTwin(owner,postBody,deviceName, counter):
    
    
    url = "35.235.92.92:4000"    
    channelName = "common"
    smartContractName = "digitalTwin"
    
    # check if newcreateDigitalTwin token needed
    authToken = getToken()

    print("AuthToken: ",authToken)

    headers = {
    'Content-Type':'application/json',
    'Accept':'application/json',
    }

    headers['Authorization'] = 'Bearer ' + authToken

    #create DT
    
    body = {
    "peers": ["peer0.machine1.manufacturers.org"],
    "fcn": "createDT",
    "args": [postBody]
    }
    
    postURL = "http://{}/channels/{}/chaincodes/{}".format(url, channelName, smartContractName)
    response = requests.post(postURL, data=json.dumps(body), headers=headers)
    print("Response for creating DT", response)
    
    timestamp=time.time()
    date_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print("@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-")
    print("Logging...")
    print('Timestamp: ',timestamp)
    print("Response: ", response)
    print("@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-")
    with open('writeLog', 'a') as logFile:
        logFile.write("{}. Transaction Time Epoch [{}] - [{}]: -> Response: {}".format(counter, timestamp, date_time, str(response)))                
        logFile.write('\n')
    
    return response  
                    
    

def getBodyCreateJsonFormat(digitalTwinInfo):
    owner= digitalTwinInfo['Static'].get('Owner','default')
    MACAddress=str(digitalTwinInfo['Static'].get('MAC Address', '0'))
    deviceName=digitalTwinInfo['Static'].get('Hostname', 'RPI-default')+'-'+MACAddress
    serialNumber=digitalTwinInfo['Static'].get('Serial Number', '0')
    manufacturer=digitalTwinInfo['Static']['Manufacturer'].get('Manufacturer', '0')
    hardware=digitalTwinInfo['Static'].get('Hardware', '0')
    memorySize=digitalTwinInfo['Static']['Manufacturer'].get('RAM', '0')
    osInfo=digitalTwinInfo['Static']['OS'].get('Name', '0')
    price=digitalTwinInfo['Static']['Manufacturer'].get('Price', '0')
    dynamicParams=str(digitalTwinInfo['Dynamic'])
    x = "{\"deviceName\":\""+deviceName+"\",\"owner\":\""+owner+"\",\"state\":\"active\",\"MACAddress\":\""+MACAddress+"\",\"serialNumber\":\""+serialNumber+"\",\"manufacturer\":\""+manufacturer+"\",\"hardware\":\""+hardware+"\",\"memorySize\":\""+memorySize+"\",\"osInfo\":\""+osInfo+"\",\"staticIP\":\"0.0.0.0\",\"price\":\""+price+"\",\"dynamicParams\":\""+dynamicParams+"\"}"
    return x

def getBodyUpdateJsonFormat(digitalTwinInfo):
    dynamicParams=str(digitalTwinInfo['Dynamic'])
    return dynamicParams

def updateDigitalTwin(digitalTwinInfo, ID, deviceName, counter):
     
    owner= digitalTwinInfo['Static'].get('Owner','default')
    
    url = "35.235.92.92:4000"    
    channelName = "common"
    smartContractName = "digitalTwin"
    
    # check if new token needed
    authToken = getToken()                                                                                                                                                                                                                     

    print("AuthToken: ",authToken)

    headers = {
    'Content-Type':'application/json',
    'Accept':'application/json',
    }

    headers['Authorization'] = 'Bearer ' + authToken

    #update DT
    
    body = {
    "peers": ["peer0.machine1.manufacturers.org"],
    "fcn": "updateAsset",
    "args": [ID, owner , getBodyUpdateJsonFormat(digitalTwinInfo)]
    }
    
    postURL = "http://{}/channels/{}/chaincodes/{}".format(url, channelName, smartContractName)
    response = requests.post(postURL, data=json.dumps(body), headers=headers)
    print("Response for updating DT", response.json()['message'])
    
    timestamp=time.time()
    date_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print("@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-")
    print("Logging...")
    print('Timestamp: ',timestamp)
    print("Response: ", response)
    print("@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-")
    with open('writeLog', 'a') as logFile:
        logFile.write("{}. Transaction Time Epoch [{}] - [{}]: -> Response: {}".format(counter, timestamp, date_time, str(response)))                
        logFile.write('\n')

def getID(response, deviceName, owner):
    
    url = "35.235.92.92:4000"    
    channelName = "common"
    smartContractName = "digitalTwin"
    headers = {
    'Content-Type':'application/json',
    'Accept':'application/json',
    }
    authToken = getToken()

    headers['Authorization'] = 'Bearer ' + authToken
    
    if response.status_code==200 and response.json()['success']==False:
        ID=response.json()['message'].split(' ')[-1]
        return ID, False
    if response.status_code==200 and response.json()['success']==True:
        body = {
            "peers": ["peer0.machine1.manufacturers.org"],
            "fcn": "getAssetbyOwner",
            "args": ["{\"owner\":\""+owner+"\"}"]
            }

        postURL = "http://{}/channels/{}/chaincodes/{}".format(url, channelName, smartContractName)
        response1 = requests.post(postURL, data=json.dumps(body), headers=headers)
        if response1.status_code==200:
            responseJson = response1.json()
            
            devices= responseJson['response']['Record']
            for device in devices:
                if device['Record']['deviceName']==deviceName:
                    digitalTwinID = open('digitalTwinID.txt', 'w+')
                    digitalTwinID.write(device['Record']['id'])
                    digitalTwinID.close()
                    return device['Record']['id'], True
        
    return '0', True

def handleCreateAndUpdate(digitalTwinInfo, counter):
    owner=digitalTwinInfo['Static'].get('Owner', 'default')
    try:
        deviceName=digitalTwinInfo["Static"].get('deviceName')
        digitalTwinID = open('digitalTwinID.txt', 'r')
        ID = digitalTwinID.readline() 
        updateDigitalTwin(digitalTwinInfo, ID, deviceName, counter)
        digitalTwinID.close()
    except:
        deviceName=digitalTwinInfo["Static"].get('deviceName')
        postURLBody = getBodyCreateJsonFormat(digitalTwinInfo)
        response = createDigitalTwin(owner, postURLBody,deviceName, counter)
        ID,flag = getID(response, deviceName, owner)
        if not flag:
            updateDigitalTwin(digitalTwinInfo, ID, deviceName, counter)
            

def writeData(digitalTwinInfo, counter):
#     print(type(digitalTwinInfo))
    print(digitalTwinInfo)
    handleCreateAndUpdate(digitalTwinInfo, counter)
    return ''

#     digitalTwinInfo_json = json.dumps(digitalTwinInfo, ensure_ascii=False)
#     print(digitalTwinInfo_json)
# 
#     url = "35.235.92.92:4000"    
#     channelName = "common"
#     smartContractName = "digitalTwin"
#     
#     # removed Token
#     authToken = accessNewToken()
# 
#     print("AuthToken: ",authToken)
# #     t = time.time() 
# #     timestamp = int(time.time()*1000.0)
# 
#     headers = {
#     'Content-Type':'application/json',
#     'Accept':'application/json',
#     }
# 
#     headers['Authorization'] = 'Bearer ' + authToken
# 
#     body = {
#     'peers': ['peer2.machine1.clientMachine.chainrider.io'],
#     'fcn': 'insertAsset',
#     'args': [str(timestamp), json.dumps(digitalTwinInfo, ensure_ascii=False)],
#     }
# 
#     postURL = ''
#     postURL = "http://{}/channels/{}/chaincodes/{}".format(url, channelName, smartContractName)
#     response = requests.post(postURL, data=json.dumps(body), headers=headers)
#     # print("Timestamp: ",timestamp)
#     # print("Response: ",response)
# 
#     date_time = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
#     print("@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-")
#     print("Logging...")
#     print('Timestamp: ',timestamp)xyzz
#     print("Response: ", response)
#     print("@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-")
#     with open('writeLog', 'a') as logFile:
#         logFile.write("{}. Transaction Time Epoch [{}] - [{}]: -> Response: {}".format(counter, timestamp, date_time, str(response)))                
#         logFile.write('\n')
# 
#     return response

'''
digitalTwinInfo =   {
                        "name": "Automation Trial",
                        "machine": "laptopWindows",
                        "city": "Tempe"
                    }
'''

digitalTwinInfo =   {"name": "TrialAGain", "machine": "laptopWindows", "city": "Tempe", "age":100}

if __name__=="__main__":
    # dt = {'Static':{'MAC Address':{'Ethernet':'b8:27:eb:59:c4:b8','Wireless':'b8:27:eb:0c:91:ed'},'Serial Number':'000000006559c4b8','Hardware':'BCM2835','Manufacturer':{'Code':'a02082','Model':'3B','Revision':1.2,'RAM':'1GB','Manufacturer':'Sony UK'},'Owner':'Blockchain Research Lab','OS':{'Name':'Raspbian GNU/Linux','Type':'debian','Version Number':'11','Architecture':'armv7l','Version':'#1459 SMP Wed Oct 6 16:41:10 BST 2021','Release':'5.10.63-v7+'},'Hostname':'raspberrypi'},'Dynamic':{'IP Addressing':{'DeviceIP':'192.168.0.107','BroadcastIP':'192.168.0.255','Netmask':'255.255.255.0','GatewayIP':'192.168.0.1','DNS_Info':{'68.105.28.11':{'Binary_Format':'44691c0b','Name':'cdns1.cox.net','Alias List':[]},'68.105.29.11':{'Binary_Format':'44691d0b','Name':'cdns6.cox.net','Alias List':[]},'68.105.28.12':{'Binary_Format':'44691c0c','Name':'cdns2.cox.net','Alias List':[]}}},'timestamp':'2021-12-01 20:13:29'}}
    # writeData(dt,0)
    pass