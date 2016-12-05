# -*- coding: utf-8 -*-
"""
Example of use Hopfield Recurrent network
=========================================

Task: Recognition of letters

"""

import numpy as np
import neurolab as nl
def comparashon(data):
        comparacion=[]
        for persona in data: #data puede ser un diccionario que contenga la lista con las fotos 
            for cosa in  data[persona]:
                print cosa                      
            target=data[persona] #esta es la lista de listas que contiene las fotos en 1 y -1
            target = np.asfarray(target) #esto se hace porque si
            net = nl.net.newhop(target) #se abre la net
            fototomada=cv2.imread("db/"+nombrecarpeta+"/"+"10"+".jpg",0)
            fototomada=cv2.medianBlur(imagen,5)
            imagen_thresh=cv2.adaptiveThreshold(fototomada,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
            cv2.imwrite("db/"+nombrecarpeta+"/"+str(10)+"thresh.jpg",imagen_thresh) 
            imagen=Image.open("db/"+nombrecarpeta+"/"+str(10)+"thresh.jpg")
            matriz = numpy.array(imagen)
            matriz_de_foto=[]
            for fila in matriz:  
                for pixel in fila:
                    if pixel<(255/2):
                        matriz_de_foto.append(-1)
                    else:
                        matriz_de_foto.append(1)
            out = net.sim([matriz_de_foto]) # se inicia la ocmparacion
            contador=0 
            for i in range(10): #se recorre cada 1 de las 10 fotos para ver si se parece o no
                ToF=((out[0] == target[i]).all(), 'Sim. steps',len(net.layers[0].outs)) #aqui tira true si se parece o false si no
                if ToF==True:
                    contador+=1 #entre mas true tire, el contador va sumando puntos
            comparacion.append([contador,persona]) #finalizada las comparaciones se añade a una lista equisde
        comparacion.sort() #de menor a mayor trues
        comparacion.reverse() #de mayor a menor
        print comparacion
        resultado=comparacion[0][1] #el resultado equisde
        print resultado
