from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import Tkinter as tki
import threading
import datetime
import imutils
import cv2
import os

class PhotoBoothApp:
	def __init__(self, vs):
		self.vs = vs
		self.frame = None
		self.thread = None
		self.stopEvent = None

		self.root = tki.Tk()
		self.panel = None

		self.root.resizable(0,0)
		self.root.config(bg="grey")
		self.root.geometry("324x471")

		#IMAGENES
		fondo = ImageTk.PhotoImage(file="gui/imgs/fondis.gif")
		cap = ImageTk.PhotoImage(file="gui/imgs/captu.gif")
		cap2 = ImageTk.PhotoImage(file="gui/imgs/captu2.gif")
		nomb = ImageTk.PhotoImage(file="gui/imgs/nom.gif")
		depto = nomb #es temporal

		fon = tki.Label(self.root, image = fondo, bg="white")
		fon.image = fondo
		fon.place(x=-1,y=-1)

		self.btn = tki.Button(self.root, image=cap, command=self.takeSnapshot)
		self.btn.image = cap
		self.btn.place(x=-2, y=386)
		self.btn.configure(state="disabled")

		#self.btn2 = tki.Button(self.root, text="Comparar!",
		#	command=self.takeSnapshot)
		#self.btn2.configure(state="disabled")


		#self.btn2.pack(side="bottom", fill="both", expand="yes", padx=10,
		#	pady=10)
                
		lb = tki.Label(self.root, image=nomb)
		lb.image = nomb
		lb.place(x=-1,y=247)
		
		lb2=tki.Label(self.root, image=depto)
		lb2.image=depto
		lb2.place(x=-1,y=310)

		self.txt = tki.Entry(self.root, width=37)
		self.txt.place(x=10,y=287)
		
		self.dep=tki.Entry(self.root,width=37)
		self.dep.place(x=10,y=350)

		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()

		self.root.wm_title("Check4Face! BETA v1.0")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoLoop(self):
		face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
		eyes_cascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')

		try:
			while not self.stopEvent.is_set():
				self.frame = self.vs.read()
				self.frame = imutils.resize(self.frame, width=300)

				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

				gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
				faces = face_cascade.detectMultiScale(gray, 1.3, 5)
				eyes = eyes_cascade.detectMultiScale(gray, 1.3, 5)

				if len(faces) != 0:
					for (x,y,w,h) in faces:
						self.temp_frame = gray[y:y+h,x:x+w]
						cv2.rectangle(image,(x,y),(x+w,y+h),(125,255,0),2)

					for (x,y,w,h) in eyes:
    						cv2.circle(image,(x+w/2,y+h/2),w/2,(255,128,0),2)
					self.btn.configure(state="normal")
				else:
					self.btn.configure(state="disabled")

				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)

				if self.panel is None:
					self.panel = tki.Label(image=image)
					self.panel.image = image
					self.panel.place(x=10,y=10)

				else:
					self.panel.configure(image=image)
					self.panel.image = image

		except RuntimeError, e:
			print("[INFO] RuntimeError")

	def takeSnapshot(self):
		nombre = self.txt.get() # Recupera el nombre de la caja de texto
		nombre = nombre.lower().split(" ") # Corta el nombre por palabras
		for n in range(len(nombre)): #Recorre cada palabra que compone el nombre
			if n == 0: # La primera palabra inicia la variable
				dirr = nombre[0]
			else: # Las siguientes palabras se van agregando con guion bajo
				dirr = dirr + "_" + nombre[n]

		if not os.access("db/"+dirr, os.F_OK): # Si no existe el directorio lo crea
			os.mkdir("db/"+dirr)
		archivos=os.listdir("db/"+dirr) #Cuenta la cantidad de imagenes existentes en el directorio
		filename = str(len(archivos)) + ".jpg" #El nombre del nuevo archivo es el numero de archivos en el directorio
		
		if  len(archivos)==0: #asi solo agrega la primera vez que se toma una foto a la persona
			departamento= self.dep.get()
			registro=open("data/empleados.txt","a")
			registro.write(self.txt.get()+"-"+departamento)
			registro.close()

		cv2.imwrite("db/"+dirr+"/"+filename, self.temp_frame.copy()) #Guarda el rostro de la persona en el archivo
		print("[INFO] Guardado {}".format(filename)) #Imprime el resultado

	def onClose(self):
		print("[INFO] Cerrando...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()
