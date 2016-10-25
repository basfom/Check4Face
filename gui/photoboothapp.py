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

		self.btn = tki.Button(self.root, text="Capturar!",
			command=self.takeSnapshot)
		self.btn.configure(state="disabled")
		
		self.btn2 = tki.Button(self.root, text="Comparar!",
			command=self.takeSnapshot)
		self.btn2.configure(state="disabled")
		
		self.btn.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)
		self.btn2.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)
				
		lb = tki.Label(self.root, text="Nombre:")
		self.txt = tki.Entry(self.root)
		self.txt.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)
		lb.pack(side="bottom", expand="yes", padx=10,
			pady=5)


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
						self.temp_frame = self.frame[y:y+h,x:x+w]
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
					self.panel.pack(side="left", padx=10, pady=10)
		
				else:
					self.panel.configure(image=image)
					self.panel.image = image

		except RuntimeError, e:
			print("[INFO] RuntimeError")

	def takeSnapshot(self):
		nombre = self.txt.get()
		nombre = nombre.lower().split(" ")
		dirr = nombre[0]+"_"+nombre[1]
		
		if os.access("db/"+dirr, os.F_OK):
			pass
		else:
			os.mkdir("db/"+dirr)
			
		archivos=os.listdir("db/"+dirr)
		filename = str(len(archivos)) + ".jpg"
		
		cv2.imwrite("db/"+dirr+"/"+filename, self.temp_frame.copy())
		print("[INFO] Guardado {}".format(filename))

	def onClose(self):

		print("[INFO] Cerrando...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()