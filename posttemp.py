import time
import os
import csv
import requests
import datetime
import json
import serial
from serial.tools import list_ports

# Search serial port
ports = list_ports.comports()
devices = [info.device for info in ports]

# Open serial port
ser = serial.Serial(devices[0], 9600)


# URL to post temperature data
url = 'https://recievetempflaskapi.herokuapp.com/post'

starttime = time.time() # start time for measurement
running = True
while (running):
    try:
        nowtimeforfile = datetime.datetime.now() # nowtime data for file naming
        fileName = str(nowtimeforfile.year) + '-' + str(nowtimeforfile.month) + '-' + str(nowtimeforfile.day)  \
            + '-data.csv' # create file name by datetime
        
        nowtime = time.time() # get nowtime for measurement
        elapsedTime = round(nowtime - starttime) #  calculate elapsed time
        divTime = 2 # minuites

        if elapsedTime % (divTime * 60) == 0:
            dtNow = datetime.datetime.now()
            nowTimeTxt = dtNow.strftime('%Y-%m-%d %H:%M:%S')
            temp = float(ser.readline())
            data = [nowTimeTxt, temp]
            preJsonData = {'date' : nowTimeTxt, 'temp' : temp}
            jsonData = json.dumps(preJsonData).encode('utf-8')

            response = requests.post(url, jsonData)

            # csv file making
            if os.path.exists(fileName) == False:
                with open(fileName, 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow(['date', 'temperature'])

            else:
                with open(fileName, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
                    
        time.sleep(1)

    except KeyboardInterrupt:
        running = False

