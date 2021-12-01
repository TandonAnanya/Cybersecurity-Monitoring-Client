#! /usr/bin/env python

import json

def getManufacturerInfo(revision, filename='ModelToManufacturer.json'):
   
   try:
       f = open(filename, 'rb')
       g = open('Owner.txt','r')
       owner = g.readline()
       
   except OSError as err:
       print("OS error: {0}".format(err))
       return False
   
   with f:
       return (json.load(f)[revision]), owner


if __name__ == "__main__":
    #to run use python ManufatcurerInfo revision_num
    # Ex: python ManufatcurerInfo 0014
    import sys
    revision = sys.argv[1]
    manufacture_details = getManufacturerInfo(revision)
    if manufacture_details:        
        print(manufacture_details)
        sys.exit(0)
    else:
        print('Error')
        sys.exit(1)
    
    