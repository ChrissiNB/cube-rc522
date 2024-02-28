import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

def turn_on_led(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup()


reader = SimpleMFRC522()
LED_PIN= 11        


print("Start writing the different cube sides to the rfid")

write = False

for i in range(6):

    try:
        print("try to write cube side " + str(i+1))
        print("Hold the cube side" + str(i+1) + "to the rfid reader")
        reader.write(str(i+1))
        
        turn_on_led(LED_PIN)
        print("written cube side " + str(i+1))

    except:
        print("writing failed ... try again")
    finally:
        GPIO.cleanup()

    print("Pick up cube and dont hold it to the rfid reader within 10 seconds")
    time.sleep(10)

print("Finished")
print("Test the reading with test_read_rfid.py and check if the cube rfids are 1 to 6")
  
GPIO.cleanup()