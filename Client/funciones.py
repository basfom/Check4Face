from PIL import Image
import os
import numpy
import cv2

def ResizeImages(nombrecarpeta):
    for contador in range(10):
        print contador
        imagen=Image.open("db/"+nombrecarpeta+"/"+str(contador)+".jpg")
        imagen=imagen.resize((300,300),Image.NEAREST)
        imagen.save("db/"+nombrecarpeta+"/"+str(contador)+".jpg")


def ajustar_y_pasar_a_unos(nombrecarpeta):
    ResizeImages(nombrecarpeta)
    ImagentoLista(nombrecarpeta)

def ImagentoLista(nombrecarpeta):
    lista_final=[]
    for contador in range(10):  
        imagen=cv2.imread("db/"+nombrecarpeta+"/"+str(contador)+".jpg",0)
        imagen=cv2.medianBlur(imagen,5)
        imagen_thresh=cv2.adaptiveThreshold(imagen,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        cv2.imwrite("db/"+nombrecarpeta+"/"+str(contador)+"thresh.jpg",imagen_thresh) 
        imagen=Image.open("db/"+nombrecarpeta+"/"+str(contador)+"thresh.jpg")
        matriz = numpy.array(imagen)
        matriz_de_foto=[]
        for fila in matriz:  
            for pixel in fila:
                if pixel<(255/2):
                    matriz_de_foto.append(-1)
                else:
                    matriz_de_foto.append(1)
        lista_final.append(matriz_de_foto)
    arreglo_para_neuronas=numpy.array(lista_final)
    #archivo.write(matriz_de_foto)
    #archivo.close()
    #FALTA VER LA WEAAAAA DE COMO QUEDA CON UNOS Y CEROS EN IMAGENCITA XDXDXD
    return True

ajustar_y_pasar_a_unos("caca")
