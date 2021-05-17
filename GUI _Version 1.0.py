import threading
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
import time
from PIL import ImageTk
from PIL import Image as PilImage
import cv2
cap=cv2.VideoCapture(0)
import numpy as np
from pyzbar.pyzbar import decode
import serial
#  tkinter main window
root = tk.ThemedTk()
root.get_themes()
root.set_theme("black")             # themes names
root.title("GUI Interface of Vision Short")
root.geometry("1400x750")
root['bg'] = 'gray5'
root.minsize(1500, 700)
root.maxsize(1500, 700)
# # ttk styles
style = ttk.Style()
style.configure("style1.TFrame", background="gray5")
style.configure("style2.TFrame", background="gray10")

style.configure("style1.TLabel", background="gray10",foreground="white")
style.configure("style2.TLabel", background="gray10",foreground="purple3")
style.configure("style3.TLabel", background="gray10",foreground="purple3",borderwidth=5)
style.configure("style4.TLabel", background="gray5",foreground="DarkOrchid1")
style.configure("style5.TLabel", background="gray5",foreground="white")
style.configure("style61.TLabel", background="gray10",foreground="#f30f01")
style.configure("style6.TLabel", background="gray10",foreground="#5eff52")

style.configure("style1.TButton",background="gray",foreground="blue2",font="Times 20 bold")
style.configure("style2.TButton",background="gray",foreground="magenta3", font="Times 20 bold",relief="raised", borderwidth=5)
style.configure("style3.TButton",background="gray",foreground="green", font="Times 20 bold",relief="raised", borderwidth=5)
style.configure("style4.TButton",background="gray",foreground="red", font="Times 20 bold",relief="raised", borderwidth=5)
#defined global varable
running = False

def myfunc():
    global running
    while True:

        if running:
            var_l_2_1da.set("Welcome Starting main system control")
            time.sleep(0.5)
            var_l_2_1da.set("Reading Data Shortening File Defined By User...")
            time.sleep(0.5)
            dict = {}
            f = open("data.txt")
            for line in f:
                x = line.split("=")
                i = x[0]
                j = x[1]
                dict.update({i: j})
            f.close()
            var_l_2_1da.set("sucessfully completed")
            time.sleep(.5)
            var_l_2_1da.set("communicating Arduino ")
            arduino = serial.Serial('COM15', 9600, timeout=1)  # Connecting Arduino UNO as arduino
            time.sleep(1)  # To stable the communication
            var_l_2_1da.set("sucessfully completed")
            var_l_2_2g.set("connected")
            var_l_4_2g.set("opened")

            while True:

                _, frame = cap.read()

                frame = cv2.resize(frame, dsize=None, fx=1.49, fy=1.45, interpolation=True)
                y = 110
                x = 0
                h = 600
                w = 1200
                frame = frame[y:y + h, x:x + w]

                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = PilImage.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                Label1_1b.imgtk = imgtk
                Label1_1b.configure(image=imgtk)
                product_counter=0
                var_l_6_2g.set(product_counter)
                for barcode in decode(frame):
                    var_l_2_1da.set("Barcode detected ")

                    myData = barcode.data.decode('utf-8')
                    myColor = (0, 0, 255)
                    pts = np.array([barcode.polygon], np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pts], True, myColor, 2)
                    pts2 = barcode.rect
                    cv2.putText(frame, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)
                    y = 110
                    x = 0
                    h = 600
                    w = 1200
                    frame = frame[y:y + h, x:x + w]
                    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                    img = PilImage.fromarray(cv2image)
                    imgtk = ImageTk.PhotoImage(image=img)
                    Label1_1b.imgtk = imgtk
                    Label1_1b.configure(image=imgtk)

                    var_l_2_1da.set("checking barcode dat in our system data ")

                    x = 0
                    for items in dict:
                        if list(dict.keys())[x] in myData:
                            data_class_value = list(dict.values())[x]
                            break
                        else:
                            pass
                        x += 1
                        time.sleep(.05)
                    if x == len(dict):
                        print()
                        var_l_2_1da.set("NOT present in the exsisting data..................")
                        time.sleep(0.5)
                        var_l_2_1da.set("Try another QR code or Update the DATA..................")
                        break

                    var_l_2_1da.set("\Present in out data.........................................")
                    time.sleep(0.5)
                    var_l_2_1da.set(f"Data in Qr is  :{myData}  Sending Poition :{data_class_value}")
                    time.sleep(0.5)
                    var_l_2_1da.set("Initilizing communication to Arduino")

                    arduino.reset_input_buffer()
                    x = data_class_value
                    arduino.write(x.encode('utf-8'))
                    time.sleep(0.5)
                    while arduino.in_waiting:
                        data = arduino.readline().decode('utf-8')
                        var_l_2_1da.set(f"sent  : {x}")
                        time.sleep(0.5)
                        var_l_2_1da.set(f"received  :{data}")
                        compare_strings(data, x)
                        if compare_strings(data, x) is True:
                            var_l_2_1da.set("This is Arduino I Recived Your Request & processing your request.. ")
                            break
                        else:
                            pass

                    while arduino.in_waiting < 1:
                        pass
                    data1 = arduino.read(1).decode('utf-8')
                    # print(data1)
                    if compare_strings(data1, 'D') is True:
                        var_l_2_1da.set ("Request Acknowlwdged.. ")
                        time.sleep(0.5)
                        var_l_2_1da.set("Imormation sent to Delivery Robot")
                        time.sleep(0.5)
                        var_l_2_1da.set("Ready to Another Task")
                        time.sleep(0.5)








                if running is False:
                    arduino.close()
                    var_l_2_2g.set("Diconnected")
                    var_l_4_2g.set("opened But\n not in use")
                    break
        else:

            print("you need to press start button to open main control")
            time.sleep(0.5)
def Update():
    print("updating")
    with open("data.txt", "a") as f:
        f.write(f"{var_e_1_2b.get()}={var_e_2_2b.get()}\n")
    print("updated")
    Entry1.delete(0, END)    # to lear entry    aftr reading data
    Entry2.delete(0, END)
def clickme():
    import subprocess
    subprocess.call(['notepad.exe', 'data.txt'])
def Start():
    print("start button pressed ")
    global running
    running = True
def Stop():
    print("stop button pressed ")
    global running
    running = False
    var_l_2_1da.set("......................................................................................")
def compare_strings(a,b):
    result = True
    for i,(x,y) in enumerate(zip(a,b)):
        if x != y:
            result = False
    return result


if __name__ == "__main__":

    x = threading.Thread(target=myfunc,daemon=True)
    x.start()
# [Frame 1 ]<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    Frame_1 = ttk.Frame(root, width=975, height=725, style="style1.TFrame")
    Frame_1.grid_propagate(0)
    Frame_1.grid(row=0, column=0, padx=10, pady=15)

    Frame_1a = ttk.Frame(Frame_1, width=965, height=50, style="style2.TFrame")
    Frame_1a.grid_propagate(0)
    Frame_1a.grid(row=0, column=0, padx=5, pady=0)

    Label1_1a = ttk.Label(Frame_1a, text="                                 Main System control Panel :",
                          font="Helvitica 20 bold", style="style1.TLabel")
    Label1_1a.grid(row=0, column=0, padx=10, pady=10)

 # frame 1a ended here tat contain main system control panel

    Frame_1b = ttk.Frame(Frame_1, width=965, height=500)
    Frame_1b.grid_propagate(0)
    Frame_1b.grid(row=1, column=0, padx=5, pady=0)

    img = ImageTk.PhotoImage(PilImage.open("camneon1.png"))

    Label1_1b = ttk.Label(Frame_1b, image=img, style="style3.TLabel")
    Label1_1b.grid(row=0, column=0)


# Frame 1b ended here that contain image label  only

    Frame_1c = ttk.Frame(Frame_1, width=965, height=60, style="style2.TFrame")
    Frame_1c.grid_propagate(0)
    Frame_1c.grid(row=2, column=0, padx=5, pady=0)

    Button1_1c = ttk.Button(Frame_1c, text="    Start", style="style3.TButton", command=Start)
    Button1_1c.grid(row=0, column=1, padx=100, pady=10)

    Button2_1c = ttk.Button(Frame_1c, text="    Stop", style="style4.TButton", command=Stop)
    Button2_1c.grid(row=0, column=2, padx=100, pady=10)

    Button3_1c = ttk.Button(Frame_1c, text=" Initialize", style="style1.TButton")
    Button3_1c.grid(row=0, column=0, padx=80, pady=10)

 # Frame c ended here that contan the  stat stop button s and intilize button

    Frame_1d = ttk.Frame(Frame_1, width=965, height=60, style="style2.TFrame")
    Frame_1d.grid_propagate(0)
    Frame_1d.grid(row=3, column=0, padx=5, pady=0)

    Frame_1da = ttk.Frame(Frame_1d, width=950, height=45, style="style1.TFrame")
    Frame_1da.grid_propagate(0)
    Frame_1da.grid(row=0, column=0, padx=5, pady=2)

    Label1_1da = ttk.Label(Frame_1da, text="  Status :  ", font="Times 20 bold", style="style4.TLabel")
    Label1_1da.grid(row=0, column=0)

    var_l_2_1da = StringVar()
    var_l_2_1da.set( "....................................................................................................................................")
    Label2_1da = ttk.Label(Frame_1da, textvar=var_l_2_1da, font="Times 18 bold", style="style5.TLabel")
    Label2_1da.grid(row=0, column=1)

    Label3_1d = ttk.Label(Frame_1da, background="red", width=2)  # optional use off this lebal                          # may be used for later
    Label3_1d.grid(row=0, column=2, sticky="e")

    # frame 1d ende here that cotain the  status variable or color status

#  [ FRAME 1 ]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#  [ FRAME 2 ]<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    Frame_2 = ttk.Frame(root, width=485, height=725, style="style1.TFrame")
    Frame_2.grid_propagate(0)
    Frame_2.grid(row=0, column=1, padx=10, pady=15)

    Frame_2a = ttk.Frame(Frame_2, width=475, height=50, style="style2.TFrame")  # frame 1a
    Frame_2a.grid_propagate(0)
    Frame_2a.grid(row=0, column=0, padx=5, pady=0)

    Label1_2a = ttk.Label(Frame_2a, text="        Position control Panel :", font="Helvitica 20 bold",
                          style="style1.TLabel")
    Label1_2a.grid(row=0, column=0, padx=10, pady=10)

    Frame_2b = ttk.Frame(Frame_2, width=475, height=210, style="style2.TFrame")  # frame 1a
    Frame_2b.grid_propagate(0)
    Frame_2b.grid(row=1, column=0, padx=5, pady=0)

    var_e_1_2b = StringVar()
    var_e_2_2b = StringVar()

    Label1_2b = ttk.Label(Frame_2b, text="Update new entry", font="Times 15 bold", style="style1.TLabel")
    Label1_2b.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    Label1_2b = ttk.Label(Frame_2b, text="Enter QR Findingcode ", font="Times 15 bold", style="style2.TLabel")
    Label1_2b.grid(row=1, column=0, padx=10, pady=10)
    Label2_2b = ttk.Label(Frame_2b, text="Enter the Position        ", font="Times 15 bold", style="style2.TLabel")
    Label2_2b.grid(row=2, column=0, padx=10, pady=10)

    Entry1 = ttk.Entry(Frame_2b, textvariable=var_e_1_2b, font="Times 15 bold")
    Entry1.grid(row=1, column=1, padx=10, pady=10)

    Entry2 = ttk.Entry(Frame_2b, textvariable=var_e_2_2b, font="Times 15 bold")
    Entry2.grid(row=2, column=1, padx=10, pady=10)

    Button1_2b = ttk.Button(Frame_2b, text="Update", style="style1.TButton", command=Update)
    Button1_2b.grid(row=3, column=1, padx=0, pady=15, )

#frae 2b ende haere tha t contain  entey amount in 2 and update button

    Frame_2c = ttk.Frame(Frame_2, width=475, height=50, style="style2.TFrame")
    Frame_2c.grid_propagate(0)
    Frame_2c.grid(row=2, column=0, padx=5, pady=0)

    Label1_2c = ttk.Label(Frame_2c, text="To show all data in the file : ", font="Times 15 bold", style="style2.TLabel")
    Label1_2c.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    Button1_2c = ttk.Button(Frame_2c, text="Click Me", style="style2.TButton", command=clickme)
    Button1_2c.grid(row=0, column=1, padx=15, pady=0, sticky="e")

# frame 2c ended here that contain lebal name  and show button to open the note pad in the processs

    Frame_2d = ttk.Frame(Frame_2, width=475, height=5, style="style1.TFrame")                # thi sframe is only for spacing in the
    Frame_2d.grid_propagate(0)
    Frame_2d.grid(row=3, column=0, padx=5, pady=7)

#  frame 2d ende here  that onle use is spacing

    Frame_2e = ttk.Frame(Frame_2, width=475, height=50, style="style2.TFrame")
    Frame_2e.grid_propagate(0)
    Frame_2e.grid(row=4, column=0, padx=0, pady=0)


    Label1_2e = ttk.Label(Frame_2e, text="           External Devices Status : ", font="Times 20 bold",
                          style="style1.TLabel")
    Label1_2e.grid(row=0, column=0)

#  frame 2e ende here it contain the only show blabel that is external device
#  by mistake i didn take a frame name 2f not exist  so next 2g
    Frame_2g = ttk.Frame(Frame_2, width=475, height=240, style="style2.TFrame")
    Frame_2g.grid_propagate(0)
    Frame_2g.grid(row=6, column=0, padx=0, pady=0)

    Label1_2g = ttk.Label(Frame_2g, text="                  Arduino      :  ", font="Times 18 bold",
                          style="style2.TLabel")
    Label1_2g.grid(row=0, column=0, pady=5)

    var_l_2_2g= StringVar()
    var_l_2_2g.set(" Disconnected ")
    Label2_2g = ttk.Label(Frame_2g, textvar=var_l_2_2g, font="Times 18 bold", style="style6.TLabel")
    Label2_2g.grid(row=0, column=1)

    Label3_2g = ttk.Label(Frame_2g, text="                   Camera      :  ", font="Times 18 bold",
                          style="style2.TLabel")
    Label3_2g.grid(row=1, column=0, pady=5)

    var_l_4_2g = StringVar()
    var_l_4_2g.set(" Closed")
    Label4_2g = ttk.Label(Frame_2g, textvar=var_l_4_2g, font="Times 18 bold", style="style6.TLabel")
    Label4_2g.grid(row=1, column=1)

    Label5_2g = ttk.Label(Frame_2g, text="No of processed QR data : ", font="Times 16 bold", style="style2.TLabel")
    Label5_2g.grid(row=2, column=0, pady=5)

    var_l_6_2g= IntVar()
    var_l_6_2g.set(0)
    Label6_2g = ttk.Label(Frame_2g, textvar=var_l_6_2g, font="Times 18 bold", style="style6.TLabel")
    Label6_2g.grid(row=2, column=1)

    root.mainloop()