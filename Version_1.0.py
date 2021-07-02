"""
Author : Himanshu Raj
E-mail : himanshuraj9194@gmail.com

"""
#-------------------------------------------------------------------------------------
from time import *
from collections import defaultdict
from heapq import *
import urllib.request
import json
from pandas import *
# /////////////////////
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import serial
import threading
from tqdm import tqdm
import sys
from termcolor import colored, cprint
#-------------------------------------------------------------------------------------
def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1
def reverse(s):
  str = ""
  for i in s:
    str = i + str
  return str

# Shortest Path Algorithm

# Nodes Data ( Weighted Node Graph)
# edges = [
# #       {{Node_1 } ,{Node_2},{Distance between Them}}
#         ("S", "1", 10),
#         ("1", "2", 10),
#         ("1", "7", 20),
#         ("2", "5", 5),
#         ("2", "3", 5),
#         ("3", "4", 12),
#         ("4", "E", 5),
#         ("5", "6", 12),
#         ("6", "7", 8),
#         ("6", "4", 10),
#         # ("F", "G", 11)
#                         ]


def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))
        g[r].append((c, l))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf"), None




# test internet



def internet_on():
   try:
        response = urllib.request.urlopen('https://www.google.com/', timeout=10)
        return True
   except:
        return False

def update_qr_database():
    xls = ExcelFile('pincode.xls')
    df = xls.parse(xls.sheet_names[0])
    global dict
    dict = df.set_index('id')['value'].to_dict()
    return df

def search_in_dict(search):
    global dict
    if search in list(dict.keys()):

        return True
    else:
        return False

class bot:


    def __init__(self,channel,read, write):

        self.channelID=channel
        self.readapi = read
        self.writeapi = write

    def read_data(self,):
        conn = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" % (self.channelID,self.readapi))
        response = conn.read()
        data = json.loads(response)
        conn.close()
        return data

    def online_status(self, ):
        data=self.read_data()
        self.online_status = data['field1'] # field one is reserved for the online status
        if self.online_status == '1':
            return True
        else:
            return False
    def working_status(self, ):
        """ Returns true when bot is ready to take work if not return false """
        data=self.read_data()
        self.working_status = data['field2']  # field one is reserved for the working  status
        if self.working_status == '1':
            return True
        else:
            return False

    def send_data(self,field_no,data):
        URL=f"https://api.thingspeak.com/update?api_key={self.writeapi}&field{field_no}={data}"
        i=0
        while i<5: # try 5 times to upload data and try to confirm it
            i=i+1
            print("inloop")
            conn = urllib.request.urlopen(URL)
            rdata = self.read_data()
            field_check = f"field{field_no}"
            rdata = rdata[field_check]
            print(rdata)
            if data==rdata:
                break
            conn.close()




if __name__ == '__main__':

    # --------------VARIABLES----------------------
    edges = [
        ("A", "B", 5),
        ("A", "H", 10),
        ("B", "C", 5),
        ("B", "E", 5),
        ("C", "D", 5),
        ("D", "E", 5),
        ("D", "F", 5),
        ("E", "G", 5),
        ("F", "G", 5),
        ("G", "H", 5),
        # ("", "G", 11)
    ]
    dict = {}
    #-----------------------------------------------
    print("--------------------------------------")
    print("--------------------------------------")
    print("Testing internet connection.....")
    if internet_on() is True:
        print( "Internet Status : CONNECTED")
    else:
        print( "Internet Status : Timeout Error....")
        exit()
    # initialising robots objects
    robot1 = bot(992542,"6H04VKZX0H5UPLMI","8KTZAG0KKO18M9IV")
    robot2 = bot(1420145, "42N515LBCG37FJNQ","S2DNEV8HEBHFE3XV")
    # importing data from excel sheet make  dictonary
    print(update_qr_database())

    # initilizing loop of work
    cap = cv2.VideoCapture(0) # open camera
    while True:
        success, img= cap.read()
        for barcode in decode(img):
            Data_in_qr = barcode.data.decode('utf-8')
            myColor = (0, 0, 255)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, myColor, 2)
            pts2 = barcode.rect
            cv2.putText(img, Data_in_qr, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9, myColor, 2)
            y = 65
            x = 0
            h = 350
            w = 1100
            img = img[y:y + h, x:x + w]
            winname="Recagnised Qr "
            cv2.namedWindow(winname)  # Create a named window
            cv2.moveWindow(winname, 0,380)  # Move it to (40,30)
            cv2.imshow(winname, img)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

#           Matching data with Our data base
            Data_in_qr=int(Data_in_qr) # typecasting

            if search_in_dict(Data_in_qr) is True:
                target_node=dict[Data_in_qr]

            else:
                print("Not Found in Our Database ")
                print("Enter Manually Valid Targetd Node of For exit for next Enter ' e '")
                target_node=input()
                if target_node == 'e':
                    continue

#           Applying shortest path Algorithm
            start_node="A"
            targeted_node =target_node
            # print(start_node,target_node)
            # print(type(start_node), type(target_node))

            go_shortest_path =dijkstra(edges,start_node,targeted_node)
            make_path = lambda tup: (*make_path(tup[1]), tup[0]) if tup else ()
            go_shortest_path=make_path(go_shortest_path[1])
            go_shortest_path=listToString(go_shortest_path)
            print(f"Going shortest path : {go_shortest_path}")


            return_shortest_path=dijkstra(edges,targeted_node,"H")
            make_path2 = lambda tup: (*make_path(tup[1]), tup[0]) if tup else ()
            return_shortest_path=make_path2(return_shortest_path[1])
            return_shortest_path=listToString(return_shortest_path)
            print(f"Return Shortest path : {return_shortest_path}")

        # checking for available bot to do this work
        #
        #     if robot1.online_status() is True:
        #         if robot1.working_status() is True:
        #             robot1.send_data(3,go_shortest_path)
        #             sleep(2)
        #             robot1.send_data(4,return_shortest_path)
        #
        #             print("Work assigned to Robot 1")
        #
        #     elif robot2.online_status() is True:
        #         if robot2.working_status() is True:
        #             robot2.send_data(3,go_shortest_path)
        #             sleep(2)
        #             robot2.send_data(4,return_shortest_path)
        #
        #             print("Work assigned to Robot 2")
        #     else:
        #         print("Opps No one available try again")

            update_qr_database()

