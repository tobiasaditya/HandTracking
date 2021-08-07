import pygame
from pygame import mixer
import redis

import json

r = redis.Redis()

def play_song():
    mixer.init()
    mixer.music.load("Audio/bensound-hipjazz (online-audio-converter.com).wav")
    mixer.music.play()
    while True:
        data = r.get("OPENCV")
        #print(json.loads(data))
        # print("Press 'p' to pause, 'r' to resume")
        # print("Press 'e' to exit the program")
        # query = input("  ")
        data = json.loads(data)
        data = str(data['data'])
        # if query == 'p':
        if data == "2":
            # Pausing the music
            mixer.music.pause()     
        # elif query == 'r':
        elif data == "3":
            # Resuming the music
            mixer.music.unpause()
        # elif query == 'e':
        elif data == "6" or data == "EXIT":
            # Stop the mixer
            mixer.music.stop()
            break
        elif data == 'VOLUME LOW':
            mixer.music.set_volume(0.1)
        elif data == 'VOLUME MID':
            mixer.music.set_volume(0.5)
        elif data == 'VOLUME HIGH':
            mixer.music.set_volume(1)        

