import subprocess, sys
import pandas as pd
import json
def extractMetaInfo(metaInfo):
    dict_info={}
    tag, info= metaInfo.split(':')
    for item in info.split(","):
        item=item.strip()
        val=item.split(' ')[0]
        key=' '.join(item.split(' ')[1:])
        dict_info[key]=val
    return tag, dict_info

def extractProcessInfo(processInfo):
    header=[item for item in processInfo[6].strip().split(' ') if item]
    data=[[item for item in processInfo[i].strip().split(' ') if item] for i in range(7,17)]
    return header, data

def get_KernelProcesses():
    command_output=subprocess.check_output(['top', '-b', '-n1'])
    command_output=command_output.decode()
    command_output=command_output.split("\n")

    dict_metadata= {}
    for i in [1,3,4]:
        item = command_output[i].split(' ')
        for i in range(len(item)):
            if item[i] and item[i][-1]=='.':
                item[i] = item[i].replace('.',',')
        item = ' '.join(item)
        key, val= extractMetaInfo(item)
        dict_metadata[key]=val

    process_header, process_data = extractProcessInfo(command_output)
    
    
    df = pd.DataFrame(data=process_data, columns=process_header)
    result = df.to_json(orient="index")
    process_info = json.loads(result)
#     process_info=json.dumps(parsed, indent=4)
    
    return dict_metadata, process_info

if __name__=='__main__':
    
    get_KernelProcesses()
    