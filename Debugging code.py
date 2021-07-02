"""
Author : Himanshu Raj
E-mail : himanshuraj9194@gmail.com

"""
#-------------------------------------------------------------------------------------
import urllib.request
import json
from time import sleep
def internet_on():
   try:
        response = urllib.request.urlopen('https://www.google.com/', timeout=10)
        return True
   except:
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
        if self.online_status == "1":
            return True
        else:
            return False
    def working_status(self, ):
        """ Returns true when bot is ready to take work if not return false """
        data=self.read_data()
        self.working_status = data['field2']  # field one is reserved for the working  status
        if self.working_status == "1":
            return True
        else:
            return False

    def send_data(self,field_no,data,field_no2,data2):
        URL=f"https://api.thingspeak.com/update?api_key={self.writeapi}&field{field_no}={data}&field{field_no2}={data2}"
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
    robot1 = bot(992542,"6H04VKZX0H5UPLMI","8KTZAG0KKO18M9IV")
    robot2 = bot(1420145, "42N515LBCG37FJNQ","S2DNEV8HEBHFE3XV")

    robot1.send_data(1,"1",2,"1")
    sleep(15)
    go="hfjfifffnf"
    return_="fsfksbvskb33"

    if robot1.online_status() is True & robot1.working_status() is True:
        print("bot 1 is online")
        print("Assigning work to ROBOT 1")
        sleep(2)
        robot1.send_data(3,go,4,return_)

    elif robot2.online_status() is True & robot2.working_status() is True:
        print("robot is online ")
        print("Assigning work to ROBOT 2")
        sleep(2)
        robot2.send_data(3, go, 4, return_)
    else:
        print("No One is online PLZ re try ")

    sleep(5)
    print(robot1.read_data())
    print(robot2.read_data())