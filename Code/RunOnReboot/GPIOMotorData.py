#check status of gpio ports
import RPi.GPIO as GPIO

def getGPIOInfo():
    ports = [5,6,14,15]
    GPIO.setmode(GPIO.BCM)  
    # Setup your channel
    for port in ports:
        GPIO.setup(port, GPIO.OUT)
    # To test the value of a pin use the .input method
    channel_is_on=0
    for port in ports:
        channel_is_on = channel_is_on or GPIO.input(port)  # Returns 0 if OFF or 1 if ON

    if channel_is_on:
        label_movement='Moving'
    else:
        label_movement='Not Moving'
    return label_movement
if __name__=='__main__':
    getGPIOInfo()