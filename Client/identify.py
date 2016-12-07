#####
from __future__ import print_function
from gui.photoboothapp1 import PhotoBoothApp
from imutils.video import VideoStream
import time
from PIL import ImageTk
from PIL import Image
####
import socket

vs = VideoStream().start()
time.sleep(2.0)

# Iniciar la GUI
pba = PhotoBoothApp(vs)
pba.root.mainloop()
