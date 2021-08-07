import cv2 as cv
import mediapipe as mp
import time
import os

import handnumber
from audio import play_song
from threading import Thread
from pygame import mixer
from queue import Queue
import redis
import json
r = redis.Redis()
def rescaleFrame(frame,scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)

    return cv.resize(frame,dimensions,interpolation=cv.INTER_AREA)

cap = cv.VideoCapture(0)

mp_draw = mp.solutions.drawing_utils

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(False,min_detection_confidence=0.9)
#Ujung jempol, telunjuk, tengah, manis, kelingking
tip_id = [4,8,12,16,20]
current_time = 0
past_time = 0

FOLDER = "HandNumber"
files_reference = os.listdir(FOLDER)
#print(files_reference)

image_file = []

#Gestur
jempol = False
telunjuk = False
tengah = False
manis = False
kelingking = False

# for image in files_reference:
#     read_image = cv.imread(f'{FOLDER}/{image}')
#     image_file.append(read_image)

def input_data():
    hasil_angka = 404
    action = 'Init'
    redis_data = {"data":"init"}
    r.set("OPENCV",json.dumps(redis_data))
    while True:
        jempol = False
        telunjuk = False
        tengah = False
        manis = False
        kelingking = False
        success, frame = cap.read()
        frame_resized = rescaleFrame(frame)
        frame_rgb = cv.cvtColor(frame_resized,cv.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)
        #print(results.multi_hand_landmarks)

        if results.multi_hand_landmarks:
            for single_hand in results.multi_hand_landmarks:
                pos_all_landmark = []
                jari_berdiri = [jempol,telunjuk,tengah,manis,kelingking]
                for id,landmark in enumerate(single_hand.landmark):
                    #print(id,landmark)

                    height, width, channel = frame_resized.shape
                    cx,cy = (width*landmark.x,height*landmark.y)
                    pos_all_landmark.append([id,cx,cy])
                    
                
                mp_draw.draw_landmarks(frame_resized,single_hand,mp_hands.HAND_CONNECTIONS)
            #print(pos_all_landmark)
            if pos_all_landmark[4][2] < pos_all_landmark[18][2]:
                jempol = True

            if pos_all_landmark[8][2] < pos_all_landmark[6][2]:
                telunjuk = True
            
            if pos_all_landmark[12][2] < pos_all_landmark[10][2]:
                tengah = True

            if pos_all_landmark[16][2] < pos_all_landmark[14][2]:
                manis = True
            
            if pos_all_landmark[20][2] < pos_all_landmark[18][2]:
                kelingking = True

            jari_berdiri = [jempol,telunjuk,tengah,manis,kelingking]
            hasil_angka = handnumber.processing_result_handsign(jari_berdiri)
            

        #cv.putText(frame_resized,str(int(fps)),(10,70),cv.FONT_HERSHEY_COMPLEX,3,(0,0,255),3)
        redis_data['data']=hasil_angka
        r.set("OPENCV",json.dumps(redis_data))

        #Teks action
        if hasil_angka == 1:
            action = 'START'
        elif hasil_angka == 2:
            action = 'PAUSE'
        elif hasil_angka == 3:
            action = 'RESUME'
        elif hasil_angka == 6:
            action = 'STOP'
        elif hasil_angka == 5:
            action = 'EXIT'

        #Tampilin hasil angka
        cv.putText(frame_resized,str(hasil_angka),(10,150),cv.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
        #Tampilin action
        cv.putText(frame_resized,f"Action : {str(action)}",(10,50),cv.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
        


        cv.imshow("Image",frame_resized)
        if cv.waitKey(1) & 0xFF==ord('d'):
            redis_data['data']="EXIT"
            r.set("OPENCV",json.dumps(redis_data))
            break
    cap.release()
    cv.destroyAllWindows()

def master_song():
    while True:
        data_redis = r.get("OPENCV")
        data = json.loads(data_redis)
        data = str(data['data'])
        print(data)
        if data =="1":
            play_song()
        elif data == "EXIT":
            r.delete("OPENCV")
            break
        


t1 = Thread(target = input_data)
t2 = Thread(target = master_song)
t1.start()
t2.start()
  