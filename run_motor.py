import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22
 
for _ in range(2):
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)
    
    print("Going forwards")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    
    sleep(4.5)
    
    print("Going backwards")
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    
    sleep(4.5)
 
print("Now stop")
GPIO.output(Motor1E,GPIO.LOW)
 
GPIO.cleanup()

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

GPIO.setup(6, GPIO.OUT) # output rf

# Initial state for LEDs:
# print("Testing RF out, Press CTRL+C to exit")

# try:
#      print("set GIOP high")
#      GPIO.output(6, GPIO.HIGH)
#      time.sleep(5)               
# except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
#    print("Keyboard interrupt")

# except:
#    print("some error") 

# finally:
#    print("clean up") 
#    GPIO.cleanup() # cleanup all GPIO 