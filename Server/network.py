# -*- coding: utf-8 -*-
"""
Example of use Hopfield Recurrent network
=========================================

Task: Recognition of letters

"""

import numpy as np
import neurolab as nl
comparacion=[]
for persona in data: #data puede ser un diccionario que contenga la lista con las fotos 
    target=data[persona] #esta es la lista de listas que contiene las fotos en 1 y -1
    target = np.asfarray(target) #esto se hace porque si
    net = nl.net.newhop(target) #se abre la net
    fototomada=#supuesta foto tomada, matriz de -1 y 1
    out = net.sim([fototomada]) # se inicia la ocmparacion
    contador=0 
    for i in range(10): #se recorre cada 1 de las 10 fotos para ver si se parece o no
        ToF=((out[0] == target[i]).all(), 'Sim. steps',len(net.layers[0].outs)) #aqui tira true si se parece o false si no
        if ToF==True:
            contador+=1 #entre mas true tire, el contador va sumando puntos
    comparacion.append([contador,persona]) #finalizada las comparaciones se añade a una lista equisde
comparacion.sort() #de menor a mayor trues
comparacion.reverse() #de mayor a menor
resultado=comparacion[0][1] #el resultado equisde
