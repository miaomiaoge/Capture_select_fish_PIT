import os
import serial 
import winsound
import pandas as pd
import playsound
import cv2
import csv

import time
import threading
from queue import Queue
from datetime import datetime

Cand_Path = "Cand_ID.xlsx"

if os.path.splitext(Cand_Path)[-1] == ".csv":
    df = pd.read_csv(Cand_Path,encoding="utf-8")
if os.path.splitext(Cand_Path)[-1] == ".xlsx":
    df = pd.read_excel(Cand_Path)

Cand_ID=list(df["ID"])
Cand_Family=list(df["Family"])

print("Cand_ID:",Cand_ID)

duration=1000
freq=1440

def Alarm(cand_id,cand_family):
            
    if cand_family== "GS3":
        print("*****************************************************************************************")
        print("*****************************************************************************************")
        print("-----------------------------------------------------------------------------------------")
        print("**********************    请注意！！！{}是候选群体{}    ********************".format(cand_id,cand_family))
        print("-----------------------------------------------------------------------------------------")
        print("*****************************************************************************************")
        print("*****************************************************************************************")
        winsound.Beep(freq,duration)
        playsound.playsound(".\voice\GS3.mp3")
        print("\n\n")

    elif cand_family== "GS6":
        print("*****************************************************************************************")
        print("*****************************************************************************************")
        print("-----------------------------------------------------------------------------------------")
        print("*******************************    请注意！！！{}是候选群体{}    **************************".format(cand_id,cand_family))
        print("-----------------------------------------------------------------------------------------")
        print("*****************************************************************************************")
        print("*****************************************************************************************")
        winsound.Beep(freq,duration)
        playsound.playsound(".\voice\GS6.mp3")
        print("\n\n")

    elif cand_family== "GS7":
        print("*****************************************************************************************")
        print("*****************************************************************************************")
        print("-----------------------------------------------------------------------------------------")
        print("*******************************    请注意！！！{}是候选群体{}    **************************".format(cand_id,cand_family))
        print("-----------------------------------------------------------------------------------------")
        print("*****************************************************************************************")
        print("*****************************************************************************************")
        winsound.Beep(freq,duration)
        playsound.playsound(".\voice\GS7.mp3")
        print("\n\n")

    elif cand_family== "GS11":
        print("*****************************************************************************************")
        print("*****************************************************************************************")
        print("-----------------------------------------------------------------------------------------")
        print("*******************************    请注意！！！{}是候选群体{}    **************************".format(cand_id,cand_family))
        print("-----------------------------------------------------------------------------------------")
        print("*****************************************************************************************")
        print("*****************************************************************************************")
        winsound.Beep(freq,duration)
        playsound.playsound(".\voice\GS11.mp3")
        print("\n\n")
    elif cand_family== "GS":
        print("*****************************************************************************************")
        print("*****************************************************************************************")
        print("-----------------------------------------------------------------------------------------")
        print("*******************************    请注意！！！{}是候选群体{}    **************************".format(cand_id,cand_family))
        print("-----------------------------------------------------------------------------------------")
        print("*****************************************************************************************")
        print("*****************************************************************************************")
        winsound.Beep(freq,duration)
        playsound.playsound(".\voice\Alarm.mp3")
        print("\n\n")

Flag = True 
Qd=Queue()
Tag_time='2017-07-17 06:03:00'
Today=datetime.now().strftime('%Y%m%d')
save_dir=os.path.join("Collection_Data",Today)
if not os.path.exists(save_dir):
    os.makedirs(save_dir) 

def write_csv(csv_path,data_row):
    with open(csv_path,'a+',newline='') as f:
        csv_write = csv.writer(f)
        if not os.path.getsize(csv_path):
            cvs_head=["ID","Date"]
            csv_write.writerow(cvs_head)
        csv_write.writerow(data_row)
  
def Cap_tag():

    global Qd, Flag,Tag_time

    baudrate=9600
    port ="COM5"
    ser = serial.Serial(port, baudrate,timeout=1)

    while True:
        if not Flag:
            return
        data = ser.readline().decode().strip()
        if data :
            data = data[1:19]   
            Tag_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            data_row=[str(data),Tag_time]
            write_csv(os.path.join(save_dir,"Fish_PIT_ID.csv"),data_row)
            Qd.put(data)
            
def shot():
    cap = cv2.VideoCapture(0) 
       
    cap.set(3,1920)
    cap.set(4,1080)
    font = cv2.FONT_HERSHEY_SIMPLEX

    global Qd, Flag,Tag_time
   
    TXT=''
    Dis=False
    while (cap.isOpened()):  
        ret_flag, Vshow = cap.read() 
        cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        datet=cur_time
        datet=datet.replace(" ","").replace(":","")
        if Qd.qsize():
            Dis=True
            TXT=Qd.get()
        if (datetime.strptime(cur_time, "%Y-%m-%d %H:%M:%S")-datetime.strptime(Tag_time,"%Y-%m-%d %H:%M:%S")).seconds>5:
            TXT=''
        
        if TXT in Cand_ID and Dis:
            idx=Cand_ID.index(TXT)
            cand_family= Cand_Family[idx]
            Dis=False
            t=threading.Thread(target=Alarm,args=(TXT,cand_family))
            t.start() 

        Vshow= cv2.putText(Vshow, cur_time, (5, 20), font, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
        Vshow= cv2.putText(Vshow, TXT, (200, 20), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("Capture_Test", Vshow)  

        k = cv2.waitKey(1) & 0xFF  
        if k == ord('s'):  
            
            pic_name=datet
            if TXT!='':
                pic_name =TXT
            cv2.imwrite(os.path.join(save_dir,pic_name+".jpg"), Vshow)
            print("图片长度：{};  宽度：{}".format(int(cap.get(3)),int(cap.get(4)))) 
            print("保存位置：.\{}\{}.jpg".format(save_dir,pic_name))
            print("------------------------------------------------------------------")
            playsound.playsound(".\voice\shotting.mp3") 
    
        if k == ord('q'):  
            Flag=False
            break

    cap.release() 
    cv2.destroyAllWindows()  
    
if __name__ == "__main__":
    
    t1= threading.Thread(target=shot,args=())
    t2= threading.Thread(target=Cap_tag,args=())
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("<=======================================================================>")
    print("<=======================================================================>")
    print("<---------------        程序运行结束 ，欢迎下次使用        ------------->")
    print("<=======================================================================>")
    print("<=======================================================================>")
