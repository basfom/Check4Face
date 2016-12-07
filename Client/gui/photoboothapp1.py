from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import Tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
import subprocess
import time
import tkMessageBox

class PhotoBoothApp:
	def __init__(self, vs):
		self.tki = tki
		self.vs = vs
		self.frame = None
		self.thread = None
		self.stopEvent = None
		self.flag_global = True

		self.training = False
		self.stops = False
		self.barrera = True
		self.foto_activated = True

		self.root = tki.Tk()
		self.panel = None
		self.panel2 = None

		self.root.resizable(0,0)
		self.root.config(bg="grey")
		self.root.geometry("655x250")

		#IMAGENES
		re=ImageTk.PhotoImage(file="gui/imgs/reen.gif")
		im=ImageTk.PhotoImage(file="gui/imgs/si,soyyo.gif")
		fondo = ImageTk.PhotoImage(file="gui/imgs/fondo2.gif")
		depl = ImageTk.PhotoImage(file="gui/imgs/deplabel.jpeg")
		noml = ImageTk.PhotoImage(file="gui/imgs/nomlabel.jpeg")
		fon = tki.Label(self.root, image = fondo, bg="white")
		fon.image = fondo
		fon.place(x=-1,y=-1)

		self.btn = tki.Button(self.root, image=re,command=self.rentrenar) #SE TIENE QUE DEFINIR ESTA WEA
		self.btn.image = re
		self.btn.place(x=322, y=183)
		self.btn.configure(state="disabled")

		self.yo = tki.Button(self.root, image=im,command=self.actualizar_reg)
		self.yo.image=im
		self.yo.place(x=434,y=183)
		self.yo.configure(state="disabled")

		self.depvar = tki.StringVar()
		self.nomvar = tki.StringVar()

		self.deplabel = tki.Label(self.root, textvariable=self.depvar, font=("Courier", 15))
		self.deplabel.place(x=389,y=129)

		self.nomlabel = tki.Label(self.root, textvariable=self.nomvar, font=("Courier", 15))
		self.nomlabel.place(x=387,y=48)


		#self.top.withdraw()

		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()

		self.root.wm_title("Check4Face! Identifier")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoLoop(self):
		face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
		eyes_cascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')

		try:
			bandera=True
			while not self.stopEvent.is_set():
				if not self.training:
					self.frame = self.vs.read()
					self.frame = imutils.resize(self.frame, width=300)
					image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

					gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
					faces = face_cascade.detectMultiScale(gray, 1.3, 5)
					#eyes = eyes_cascade.detectMultiScale(gray, 1.3, 5)
					if len(faces) != 0:


						for (x,y,w,h) in faces:
							self.temp_frame = gray[y:y+h,x:x+w]
							cv2.rectangle(image,(x,y),(x+w,y+h),(125,255,0),2)

						#for (x,y,w,h) in eyes:
						#		cv2.circle(image,(x+w/2,y+h/2),w/2,(255,128,0),2)
						#if self.flag_global == True:
						#	self.btn.configure(state="normal")
						if bandera:
							cv2.imwrite("./identificador/comparative.png", self.temp_frame.copy())
							output = subprocess.Popen("../openface/demos/classifier.py infer ../Server/info/classifier.pkl ./identificador/comparative.png", shell=True, bufsize=100000, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,close_fds=True)
							out = output.stdout.read()
							if "Predict" in out:
								bandera=False
								texto = out.strip().split("Predict ")
								names, confidence  = texto[1].split(" with ")
								names = names.split("_")
								for i in range(len(names)):
									names[i] = names[i].capitalize()
								names = " ".join(names)
								self.names = names
								confidence = int(float(confidence[0:4]) * 100)
								confidence= str(confidence) + "%"
								self.nomvar.set(names+" ("+confidence+")")
								self.obtener_dep(names)
								self.stops = False
								self.btn.configure(state="normal")
								self.yo.configure(state="normal")
							else:
								print("Sin resultados!")


							#texto = ""
							#for letra in out:
							#	texto = texto + letra
							#	if
					else:
						pass
						#self.btn.configure(state="disabled")

					image = Image.fromarray(image)
					image = ImageTk.PhotoImage(image)

					if self.panel is None:
						self.panel = tki.Label(image=image)
						self.panel.image = image
						self.panel.place(x=10,y=10)

					else:
						if not self.stops:
							self.panel.configure(image=image)
							self.panel.image = image
				else:
					self.frame2 = self.vs.read()
					self.frame2 = imutils.resize(self.frame2, width=300)

					image2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)

					gray2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2GRAY)
					faces2 = face_cascade.detectMultiScale(gray2, 1.3, 5)

					if len(faces2) != 0:
						for (x,y,w,h) in faces2:
							self.temp_frame = gray2[y:y+h,x:x+w]
							cv2.rectangle(image2,(x,y),(x+w,y+h),(125,255,0),2)

						if self.txt2.get() != "":
							if self.barrera:
								self.btn2.configure(state="normal")
					else:
						self.btn2.configure(state="disabled")


					image2 = Image.fromarray(image2)
					image2 = ImageTk.PhotoImage(image2)

					if self.panel2 is None:
						self.panel2 = tki.Label(self.top, image=image2)
						self.panel2.image = image2
						self.panel2.place(x=10,y=10)

					else:
						self.panel2.configure(image=image2)
						self.panel2.image = image2


		except RuntimeError, e:
			pass

	def takeSnapshot(self):
		nombre = self.txt2.get() # Recupera el nombre de la caja de texto
		nombre = nombre.lower().split(" ") # Corta el nombre por palabras
		for n in range(len(nombre)): #Recorre cada palabra que compone el nombre
			if n == 0: # La primera palabra inicia la variable
				dirr = nombre[0]
			else: # Las siguientes palabras se van agregando con guion bajo
				dirr = dirr + "_" + nombre[n]

		if not os.access("db/"+dirr, os.F_OK): # Si no existe el directorio lo crea
			os.mkdir("db/"+dirr)
		archivos=os.listdir("db/"+dirr) #Cuenta la cantidad de imagenes existentes en el directorio
		filename = str(len(archivos)) + ".png" #El nombre del nuevo archivo es el numero de archivos en el directorio

		if self.flag_3FOTOS:
			self.fotos_iniciales=len(archivos)
    		self.flag_3FOTOS=False

		if self.foto_activated:
			cv2.imwrite("db/"+dirr+"/"+filename, self.temp_frame.copy()) #Guarda el rostro de la persona en el archivo
			print("[INFO] Guardado {}".format(filename)) #Imprime el resultado
			if  len(archivos)==(2+self.fotos_iniciales):
				self.foto_activated = False
		if  len(archivos)==(3+self.fotos_iniciales): #asi solo agrega la primera vez que se toma una foto a la persona
			#os.system("mkdir db_neuronas/"+dirr)
			self.btn2.configure(state="disabled")

			os.system("../openface/util/align-dlib.py ./db/"+dirr+"/ align outerEyesAndNose ./db_neuronas/"+dirr +"/ --size 96")
			os.system("../openface/batch-represent/main.lua -outDir ../Server/info/ -data ../Client/db_neuronas/")
			os.system("../openface/demos/classifier.py train ../Server/info/")

			tkMessageBox.showinfo("", "Entrenamiento completado con exito!")
			self.top.destroy()
			self.root.destroy()
			self.onClose()

			self.depvar = ""
			self.nomvar = ""
			self.training = False

			self.flag_global = False
			self.barrera = False


	def rentrenar(self):
		self.training = True

		self.flag_3FOTOS=True

		fondo2 = ImageTk.PhotoImage(file="gui/imgs/fondis2.jpeg")
		cap = ImageTk.PhotoImage(file="gui/imgs/captu.gif")

		self.top = tki.Toplevel(self.root)
		self.top.transient(self.root)
		self.top.title("Reentrenamiento - Check4Face!")
		self.top.resizable(0,0)
		self.top.config(bg="grey")
		self.top.geometry("324x407")

		fon2=tki.Label(self.top,image=fondo2,bg="white")
		fon2.image=fondo2
		fon2.place(x=-1,y=-1)

		self.txt2 = tki.Entry(self.top, width=37)
		self.txt2.place(x=10,y=289)

		self.btn2 = tki.Button(self.top,image=cap,command=self.takeSnapshot)
		self.btn2.image = cap
		self.btn2.place(x=-2, y=315)
		self.btn2.configure(state="disabled")

		self.top.mainloop()
		#self.top.state(newstate='normal')

	def onClose(self):
		print("[INFO] Cerrando...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()

	def actualizar_reg(self):
		nombre = self.names
		hora=time.strftime("%H:%M:%S")
		fecha=time.strftime("%d/%m/%y")
		archivo=open("registro.txt","a")
		archivo.close()
		archivo=open("registro.txt","r")
		temp=open("temp.txt","w")
		flag=False #se mantiene en false si no esta, no ha llegado
		for linea in archivo:
			datos=linea.strip().split("-")
			if datos[0]==nombre and len(datos)==2: #si es igual a 3 significa que ya entro y salio y se necesita crear otra linea
				horas=datos[1].split("(")
				horas=horas[1]
				horas=horas.split(")")
				horas=horas[0]
				horas,mins,segs=horas.split(":")
				horas1,mins1,segs1=hora.split(":")
				if horas==horas1:
					if (int(mins1)-int(mins))<5:
						#aqui va que no se pueda escribir
						print("Se registro hace menos de 5 minutos!")
					else:
						temp.write(linea.strip()+"-"+fecha+"("+hora+")\n")
				else:
					temp.write(linea.strip()+"-"+fecha+"("+hora+")\n")
				flag=True
			else:
				temp.write(linea)
		if flag==False:
			temp.write(nombre+"-"+fecha+"("+hora+")\n")
		archivo.close()
		temp.close()
		archivo=open("registro.txt","w")
		temp=open("temp.txt","r")
		for linea in temp:
			archivo.write(linea)
		archivo.close()
		temp.close()
		self.root.destroy()
		self.onClose()

	def obtener_dep(self, nombre):
		archivo =open ("./data/empleados.txt")
		for linea in archivo:
			datos=linea.strip().split("-")
			if nombre.lower()==datos[0].lower():
				self.depvar.set(datos[1])
				return None
		self.depvar.set("SIN RESULTADO!")
