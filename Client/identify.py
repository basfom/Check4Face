#####
from __future__ import print_function
from gui.photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import time
####

vs = VideoStream().start()
time.sleep(2.0)

# Iniciar la GUI
pba = PhotoBoothApp(vs)
pba.root.mainloop()
