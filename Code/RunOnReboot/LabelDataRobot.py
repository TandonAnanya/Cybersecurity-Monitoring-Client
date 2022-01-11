import subprocess
import RPi.GPIO as GPIO
#check status of port 2(fan)

from time import sleep

def checkEncoder():
    Counter=[0]
    
    def Interrupt(Counter):
        Counter[0] = Counter[0] + 1
        print('Counter=',str(Counter))

    
    sense_pin = 21

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(sense_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
    GPIO.add_event_detect(sense_pin, GPIO.BOTH,callback=lambda x: Interrupt(Counter),  bouncetime= 2000)
    sleep(1)
    return "Moving" if Counter[0]>0 else "Not Moving"

def getLabel():
    output=subprocess.check_output(['uhubctl','-l','1-1','-p','2'])
    output=output.decode()
    output=output.split('\n')[1].strip().split(' ')
    print(output)
    if output[3]=='power':
        label_fan='Fan on'
    elif output[3]=='off':
        label_fan='Fan off'
    else:
        label_fan='unknown'

    # #check status of gpio ports

    # ports = [5,6,14,15]
    # GPIO.setmode(GPIO.BCM)  
    # # Setup your channel
    # for port in ports:
    #     GPIO.setup(port, GPIO.OUT)
    # # To test the value of a pin use the .input method
    # channel_is_on=0
    # for port in ports:
    #     channel_is_on = channel_is_on or GPIO.input(port)  # Returns 0 if OFF or 1 if ON

    # if channel_is_on:
    #     label_movement='Moving'
    # else:
    #     label_movement='Not Moving'
    
    #setting final label

    if label_fan=='Fan off' and checkEncoder()=='Not Moving':
        final_label='idle'
    else:
        final_label=label_fan+' '+checkEncoder()
    
    return final_label

if __name__=="__main__":
    print(getLabel())
