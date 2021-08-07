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
hands = mp_hands.Hands(False,min_detection_confidence=0.75)
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
        r.set("OPENCV",hasil_angka)

        #Tampilin hasil angka
        cv.putText(frame_resized,str(hasil_angka),(10,150),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        


        cv.imshow("Image",frame_resized)
        if cv.waitKey(1) & 0xFF==ord('d'):
            break
    cap.release()
    cv.destroyAllWindows()

def master_song():
    while True:
        data = r.get("OPENCV")
        data = str(json.loads(data))
        if data =="1":
            play_song()
        elif data == "5":
            break
        


t1 = Thread(target = master_song)
t2 = Thread(target = input_data)
t1.start()
t2.start()
  