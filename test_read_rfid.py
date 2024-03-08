import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import signal

'Turn on LED'
def turn_on_led(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup()

'Stop interface with Ctrl+C'
def end_read():
    GPIO.cleanup()
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    


continue_reading = True
signal.signal(signal.SIGINT, end_read)

reader = SimpleMFRC522()
LED_PIN= 11



print("Start test rfid read")

while(continue_reading):
    try:
        uid, text_rfid = reader.read_no_block() #Read uid and text form rfid
        reader.READER.MFRC522_Anticoll() #Function to read data in every loop
        rfid = int(text_rfid) #convert rfid text to int

        if (rfid not in [1,2,3,4,5,6]): #check if the number 1 to 6 is read
            raise ValueError('Wrong rfid number write_rfid again')
            
        turn_on_led(LED_PIN) # show rfid was read

        print("id: " + str(rfid) + " uid: " + str(uid))
    except:
        print("id:  -> lay down cube")
    finally:
        GPIO.cleanup()
    
