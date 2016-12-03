from PIL import Image
import os
import numpy
def ResizeImages(nombrecarpeta):
    for contador in range(10):
        print contador
        imagen=Image.open("db/"+nombrecarpeta+"/"+str(contador)+".jpg")
        imagen=imagen.resize((300,300),Image.NEAREST)
        print "creoquefunciona"
        imagen.save("db/"+nombrecarpeta+"/"+str(contador)+".jpg")


def ajustar_y_pasar_a_unos(nombrecarpeta):
    ResizeImages(nombrecarpeta)
    ImagentoLista(nombrecarpeta)

def ImagentoLista(nombrecarpeta):
    lista_final=[]
    #GUARDAR LA LISTA DE LISTAS PARA LAS NEURONAS EN UN TXT?
    #archivo = open(nombrecarpeta+".txt", 'w')
    for contador in range(10):
        imagen=Image.open("db/"+nombrecarpeta+"/"+str(contador)+".jpg")
        matriz = numpy.array(imagen)
        matriz_de_foto=[]
        matriz_wb=[]
        for fila in matriz:
            fila=[]
            for pixel in fila :
                if pixel<(255/2):
                    matriz_de_foto.append(-1)
                    fila.append(0)
                else:
                    matriz_de_foto.append(1)
                    fila.append(255)
            matriz_wb.append(fila)
        arr = numpy.array(matriz_wb)
        imagenwb=Image.fromarray(arr.clip(0,255).astype('uint8'), 'gray')
        imagenwb.save(str(contador)+"awa.jpg")
        lista_final.append(matriz_de_foto)
        #archivo.write(matriz_de_foto)
    #archivo.close()
    #FALTA VER LA WEAAAAA DE COMO QUEDA CON UNOS Y CEROS EN IMAGENCITA XDXDXD
    return True

ajustar_y_pasar_a_unos("caca")
