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

# Shortest Path Algorithm

# Nodes Data ( Weighted Node Graph)
edges = [
#       {{Node_1 } ,{Node_2},{Distance between Them}}
        ("S", "1", 10),
        ("1", "2", 10),
        ("1", "7", 20),
        ("2", "5", 5),
        ("2", "3", 5),
        ("3", "4", 12),
        ("4", "E", 5),
        ("5", "6", 12),
        ("6", "7", 8),
        ("6", "4", 10),
        # ("F", "G", 11)
                        ]


def dijkstra(edges, f, t):
    g = defaultdict(set)
    for l, r, c in edges:
        g[l].add((c, r))
        g[r].add((c, l))

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

make_path = lambda tup: (*make_path(tup[1]), tup[0]) if tup else ()

# test internet



def internet_on():
   try:
        response = urllib.request.urlopen('https://www.google.com/', timeout=10)
        return True
   except:
        return False
dict={}
def update_qr_database():
    xls = ExcelFile('pincode.xls')
    df = xls.parse(xls.sheet_names[0])
    print(df)
    global dict
    dict = df.set_index('id')['value'].to_dict()





class bot:
    def __init__(self,channel,read, write):
        # Instance Variable
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

    print("--------------------------------------")
    print("--------------------------------------")
    print("Testing internet connection.....")
    if internet_on() is True:
        print( "Internet Status : CONNECTED")
    else:
        print( "Internet Status : Timeout Error....")
        exit()

    robot1 = bot(992542,"6H04VKZX0H5UPLMI","8KTZAG0KKO18M9IV")
    robot2 = bot(1420145, "42N515LBCG37FJNQ","S2DNEV8HEBHFE3XV")
