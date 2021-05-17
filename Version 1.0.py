import time
import winsound
import sys
from termcolor import colored, cprint

winsound.Beep(2500,100)
winsound.Beep(2500,100)
cprint("WELCOME",color='cyan',attrs=['bold','dark'], file=sys.stderr)
cprint("Object Delivery  System initializing...",color='magenta',attrs=['bold'], file=sys.stderr)

winsound.Beep(2500,100)
winsound.Beep(2500,100)


time.sleep(.4)
cprint("\nImporting All Required Module and Dependecies....  ",color='magenta',attrs=['bold'], file=sys.stderr)
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import serial
import threading
from tqdm import tqdm
import sys
from termcolor import colored, cprint

time.sleep(.4)
for i in tqdm (range (100), desc="Importing  "):
    pass
winsound.Beep(2500,100)
cprint("Importing Sucessfully Completed.",color='blue',attrs=['bold'], file=sys.stderr)
#  global variables
myData1=''
myData=''
data_class_value=''
data_class_name=''
#.....................................................................
time.sleep(0.4)
cprint("\nCommunicating with the Arduino UNO Throgh COM[15] PORT....",color='magenta',attrs=['bold'], file=sys.stderr)
arduino=serial.Serial('COM15',9600,timeout=1)                     # Connecting Arduino UNO as arduino
time.sleep(1)                                                     # To stable the communication
for i in tqdm (range (100), desc="Connecting "):
    pass
winsound.Beep(2500,100)
cprint("Communication Successfully Established",color='blue',attrs=['bold'], file=sys.stderr)
#.....................................................................
time.sleep(.4)
cprint("\nReading Data Shortening File Defined By User...",color='magenta',attrs=['bold'], file=sys.stderr)
dict={}
f=open("data.txt")
for line in tqdm(f,desc="loading ",ascii=True,ncols=105):
    x=line.split(":")
    i=x[0]
    j=x[1]
    dict.update({i:j})
f.close()
time.sleep(0.4)
for i in tqdm (range (100), desc="Loading..."):
    pass
winsound.Beep(2500,100)
cprint("Sucessfully Completed",color='blue',attrs=['bold'], file=sys.stderr)
#.......................................................................
time.sleep(0)
cprint("\nOpening Camera ...",color='magenta',attrs=['bold'], file=sys.stderr)
cap = cv2.VideoCapture(0)
for i in tqdm (range (100), desc="Opening "):
    pass
winsound.Beep(2500,1000)
cprint("Opened Sucessfully",color='blue',attrs=['bold'], file=sys.stderr)
# user defined function
def loop1():
    while True:
        success, img1 = cap.read()
        y = 65
        x = 0
        h = 350
        w = 1100
        img1 = img1[y:y + h, x:x + w]
        winname = "Live Camera Feed"
        cv2.namedWindow(winname)  # Create a named window
        cv2.moveWindow(winname, 0,0)  # Move it to (40,30)
        cv2.imshow(winname, img1)
        cv2.waitKey(1)

def loop2():
    while True:
        success, img= cap.read()
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            myColor = (0, 0, 255)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, myColor, 2)
            pts2 = barcode.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9, myColor, 2)
            y = 65
            x = 0
            h = 350
            w = 1100
            img = img[y:y + h, x:x + w]
            winname="Recagnised Qr "
            cv2.namedWindow(winname)  # Create a named window
            cv2.moveWindow(winname, 0,380)  # Move it to (40,30)
            cv2.imshow(winname, img)
            cv2.waitKey(1)
            print()
            print()
            cprint("Checking This Item In The Our Data                          ",on_color='on_cyan', attrs=['bold'], file=sys.stderr)
            x = 0
            for items in tqdm(dict,desc="Checking ",ascii=False,ncols=75):
                if list(dict.keys())[x] in myData:
                    # print(f"at position,{x},Found in the Data")
                    data_class_value = list(dict.values())[x]
                    # data_class_name  = list(dict.keys())[x]
                    # cprint("Present  In  Our Data ", color='green',on_color='on_green', attrs=['bold'], file=sys.stderr)
                    # cprint("Present  In  Our Data ", color='magenta', attrs=['bold'], file=sys.stderr)
                    break
                else:
                    pass
                x += 1
                time.sleep(.05)
            if x == len(dict):
                print()
                cprint("NOT present in the exsisting data............................", color='red',on_color='on_red', attrs=['bold'], file=sys.stderr)
                cprint("NOT present in the exsisting data",color='red', attrs=['bold'], file=sys.stderr)
                cprint("Try another QR code or Update the DATA", color='red', attrs=['bold'], file=sys.stderr)
                break
            print("            ")
            cprint("\Present in out data.........................................", color='green',on_color='on_green', attrs=['bold'], file=sys.stderr)
            cprint(f"Data in Qr is  :{myData}  Sending Poition :{data_class_value}", color='green', attrs=['bold'], file=sys.stderr)
            print("")
            cprint("Initilizing communication to Arduino                         ", on_color='on_cyan', attrs=['bold'], file=sys.stderr)
            arduino.reset_input_buffer()
            x=data_class_value
            # arduino.write(x.encode('utf-8'))
            # while arduino.in_waiting:
            #      data = arduino.read(1).decode('utf-8')
            #      print(data)
            #      if compare_strings(data, x) is True:
            #         cprint("Hey This Is Arduino \nI Have Received Your Request", attrs=['bold'], file=sys.stderr)
            #         cprint("Working on Your Request.", color='magenta', attrs=['bold'], file=sys.stderr)
            #         break
            arduino.write(x.encode('utf-8'))
            time.sleep(0.5)
            while arduino.in_waiting:
                data = arduino.readline().decode('utf-8')
                print("sent      :", x)
                print("received  :", data)
                compare_strings(data, x)
                if compare_strings(data, x) is True:
                    print("This is Arduino I Recived Your Request \nProcessing your request.. ")
                    break
                else:
                    pass
            # arduino.reset_input_buffer()
            print("This is Arduino I Recived Your Request \nProcessing your request.. ")
            while arduino.in_waiting < 1:
                pass
            data1 = arduino.read(1).decode('utf-8')
            print(data1)
            if compare_strings(data1,'D') is True:
                cprint("Request Acknowlwdged.. ", color='green',attrs=['bold'], file=sys.stderr)
                cprint("Imormation sent to Delivery Robot", attrs=['bold'], file=sys.stderr)
                cprint("Ready to Another Task", attrs=['bold'], file=sys.stderr)
                cprint(".....................................................", color='green', on_color='on_green', attrs=['bold'], file=sys.stderr)

                # arduino.reset_input_buffer()
        cprint('Searching QR......', end='',on_color='on_green', attrs=['bold'], file=sys.stderr)
        # print('Searching QR......', end='')
        time.sleep(0.2)
        for i in range(50):
            time.sleep(0.04)
            print('\b', end='')
def compare_strings(a,b):
    result = True
    for i,(x,y) in enumerate(zip(a,b)):
        if x != y:
            result = False
    return result
thread1 = threading.Thread(target=loop1)
thread1.start()

thread2 = threading.Thread(target=loop2)
thread2.start()