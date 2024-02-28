import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import os
import requests
import time
import pandas as pd



######### Functions ###########

'Find USB path where the media is stored'
def find_usb_media_path(base_path='/media/admin'):
    for entry in os.listdir(base_path):
        path = os.path.join(base_path, entry)
        if os.path.isdir(path):
            return path
    return None

'Select only the newest file in directory (if there are more than one)'
def newest_file_in_directory(directory):
    files = os.listdir(directory)
    files = [os.path.join(directory,f) for f in files if os.path.isfile(os.path.join(directory,f))]
    newest_file = max(files, key=os.path.getmtime)
    return newest_file

'Turn LED on to visualize rfid reading'
def turn_on_led(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup()

'Upload media request to backend'
def upload_media(myobj):
    print(myobj)
    url = 'http://localhost:3000/upload'

    try:
        requests.post(url, json = myobj)

    except:
        print("Server nicht erreichbar " + myobj)

'Setup stats csv'
def setup_stats(media_paths, usb_media_path):
    dict_empty_data = {
        "tag": list(media_paths.keys()),
        "count": [0] * len(media_paths.keys()),
        "total_time": [0.0] * len(media_paths.keys()),
    }

    stats_path = os.path.join(usb_media_path,"stats/data.csv")
    if not os.path.exists(stats_path):
        df = pd.DataFrame(dict_empty_data)
        df.to_csv(stats_path, index=False)

    return stats_path

'Write stats to csv'
def write_stats(stats_path, rfid_last, time_change_rfid):
    print("time to " + str(rfid_last) )
    loop_time = time.time() - time_change_rfid
    df = pd.read_csv(stats_path)
    index = df.loc[df["tag"] == rfid_last].index

    print("print cont +1")
    df.iloc[index, 1] += 1
    print("loop time " + str(loop_time) + "s")
    df.iloc[index,2] += loop_time

    print(df)
    df.to_csv(stats_path, index=False)
    time_change_rfid = time.time()
    return time_change_rfid




######### Main Code ###########

if __name__ == "__main__":

    #Setup connection to usb
    usb_media_path = find_usb_media_path() # Find path of usb stick
    print("USB media path: " + str(usb_media_path)) # print found usb path

    if usb_media_path is None: #if no usb then stop
        print("Kein USB-Stick gefunden. Bitte überprüfen Sie die Verbindung.")
        exit(1)
        #todo define alternative media folder on raspberry

    # Define Meida paths (0 is when start animation is shown)
    media_paths = {
        0: "",
        1: os.path.join(usb_media_path, "videos/Rexroth1/"),
        2: os.path.join(usb_media_path, "videos/Rexroth2/"),
        3: os.path.join(usb_media_path, "videos/Rexroth3/"),
        4: os.path.join(usb_media_path, "videos/Rexroth4/"),
        5: os.path.join(usb_media_path, "videos/Rexroth5/"),
        6: os.path.join(usb_media_path, "videos/Rexroth6/"),
    }

    #setup csv for stats
    stats_path = setup_stats(media_paths, usb_media_path)

    #inilize SimpleMFRC522 to read data from RC522
    reader = SimpleMFRC522()


    # Define variables
    continue_reading = True #while loop
    LED_PIN= 11  #pin led


    time_read_rfid = time.time()
    time_change_rfid = time.time()

    rfid_last = 0 #start with empty/start path
    objpathempty = {"filePath":""} #show empty/start obj
    upload_media(objpathempty) #requst for media path

    try:
        while continue_reading:

            try:
                uid, text_rfid = reader.read_no_block() #Read uid and text form rfid
                reader.READER.MFRC522_Anticoll() #Function to read data in every loop
                rfid = int(text_rfid) #convert rfid text to int
                if (rfid not in [1,2,3,4,5,6]): #check if the number 1 to 6 is rea
                    print("read wrong rfid text or error when reading")
                    continue

                time_read_rfid = time.time() # track time when rfid was read
                turn_on_led(LED_PIN) # show rfid was read

                print("id: " +  str(rfid)) #print id

            except:
                print('no id') # if error occurs

                if time.time() - time_read_rfid > 10: #when cube is missing for 10s
                    time_read_rfid = time.time()
                    print("rfid not read for 10 seconds -> cube is missing")
                    if (rfid_last != 0): #if rfid is different start request
                        upload_media(objpathempty)
                        time_change_rfid = write_stats(stats_path, rfid_last, time_change_rfid) #wirte the stats
                        rfid_last = 0 # set last rfid to start/empty
            finally:
                GPIO.cleanup()

            if(text_rfid == None ): #if no id is read start form top
                continue

            elif (rfid != rfid_last): #if id is read and rfid changed
                media_path = media_paths[rfid] #get media path of rfid
                objpath = {"filePath":newest_file_in_directory(media_path)} #defien object path for the media
                upload_media(objpath) # send the request for the defined pyht
                time_change_rfid = write_stats(stats_path, rfid_last, time_change_rfid) # write the stats
                rfid_last = rfid #change last rfid to read rfid

    except KeyboardInterrupt:
        print("Crtrl+C entered Code stopped") # stop code when crtrl+c
        exit(1)

