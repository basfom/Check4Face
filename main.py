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
	#fase beta
#cargamos la plantilla e inicializamos la webcam:
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
eyes_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
 
while(True):
    #leemos un frame y lo guardamos
    ret, img = cap.read()
    #print img
 
    #convertimos la imagen a blanco y negro
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    #buscamos las coordenadas de los rostros y guardamos su posicion
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    eyes = eyes_cascade.detectMultiScale(gray, 1.3, 5)
    #estructura faces
    #x inicio en x de izq a der
    #y inicio en y de arriba a abajo
    #w cuando mas avanza en x desde su inicio
    #h cuanto mas avanza en y desde su inicio
    #test ubicacion
#    cv2.rectangle(img,(50,50),(200,200),(125,255,0),2)
#    print faces
    #Dibujamos un rectangulo en las coordenadas de cada rostro
    for (x,y,w,h) in faces:
    	for (x,y,w,h) in eyes:
    		cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,0),2)
        cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,0),2)
        #print "x=", x
        #print "x+w=", x+w
        #print "y=",y
        #print "y+h=", y+h 


 
    #Mostramos la imagen
    cv2.imshow('img',img)
     
    #con la tecla 'q' salimos del programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2-destroyAllWindows()