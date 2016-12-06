import neurolab as nl
import numpy as np

def crearRed(target):
    target = np.asfarray(target)
    target[target == 0] = -1
    #Crear red
    net = nl.net.newhop()
    print net
