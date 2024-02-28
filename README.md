# cube-rc522

Read RFID tags with module rc522 on a Raspberry Pi 4

## Connect the RC522 to the Raspberry Pi 4 GPIO Pins

![Overview connect RC522 to Raspberry Pi](./doku/Übersicht%20RC522%20Pin%20Belegung.png)

![RC522 Pin allocation](./doku/RC522%20Pin%20Belegung.png)

![GPIO Pins Raspberry Pi 4](./doku/Pins%20Raspberry%20Pi.png)

If you want to check with an LED whether an RFID tag has been read, you must connect the following GPIO pins of the Raspberry Pi: <br>
Pi Pin 11 to anode of LED (+ 3.3 V) <br>
Pi Ground to cathode of LED (- GND)

RFID Reader Connection library [MFRC522 Repo](https://github.com/pimylifeup/MFRC522-python/)

## Setup for RFID Tags with cube

Place the RFID tags on every side of the cube.

To read the RFID tags the distance between the reader and the tags should be within 2 cm.

To write the sides 1 to 6 on the RFID tags use the script [write_rfid](write_rfid.py).

1. Place the 1. side of the cube on the reader
2. Wait until the RFID tag is written
3. Lift the cube and wait 10 seconds
4. Place the 2. side of the cube on the reader
5. ...

To check the written ID on the RFID tags use the script [test_read_rfid](test_read_rfid.py)

Run the interface script to send the requests to the backend of our website [interface](interface.py).
Before running you should check:

1. Is the RC522 module connected
2. Are the RFID tags for every side of the cube written form 1 to 6
3. Is the usb stick with the media files connected to the Raspberry Pi
4. Is the usb path to the media files right

   `def find_usb_media_path(base_path='/media/admin'):`

   Line 13 (Path on Raspberry Pi)

   ```
   media_paths = {
    0: "",
    1: os.path.join(usb_media_path, "videos/Rexroth1/"),
    2: os.path.join(usb_media_path, "videos/Rexroth2/"),
    3: os.path.join(usb_media_path, "videos/Rexroth3/"),
    4: os.path.join(usb_media_path, "videos/Rexroth4/"),
    5: os.path.join(usb_media_path, "videos/Rexroth5/"),
    6: os.path.join(usb_media_path, "videos/Rexroth6/"),
   }
   ```

   Line 94 to 102 (Define Folder paths for 1 to 6 on usb stick)

   Place the media files inside the folders 1 to 6 for every cube side

5. Run the frontend and backend with npm start and the interface.py with python interface.py over the command line
