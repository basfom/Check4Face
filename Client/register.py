#####
from __future__ import print_function
from gui.photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import time
####
import numpy as np
import cv2
import os
####
import socket

s = socket.socket()
flag = False

try:
    print("Probando conexion con el servidor...")
    s.connect((socket.gethostname(), 1111))
    flag = True
except:
    print("No se puede establecer la conexion con el servidor...")

while flag:
    print("Conexion establecida!")

    vs = VideoStream().start()

    # Iniciar la GUI
    pba = PhotoBoothApp(vs)
    pba.root.mainloop()

    s.send("entrenar")

    #print(s.recv(1024))
    #if mensaje == "close":
    #    break
print("Cerrando cliente")
s.close()
