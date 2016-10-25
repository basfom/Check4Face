##### 
from __future__ import print_function
from gui.photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import time
####
import numpy as np
import cv2
import os
#funciones
def crear_carpeta(nombre):
    os.mkdir(nombre)
    return "Se ha creado la carpeta"

def revisar_carpeta(nombre):
	#retorna true si existe la carpeta
	#false si no
	return os.access("Barbara Uribe", os.F_OK)

def recorrer_carpetas():
    pass


vs = VideoStream().start()
time.sleep(2.0)
# Iniciar la GUI
pba = PhotoBoothApp(vs)
pba.root.mainloop()
