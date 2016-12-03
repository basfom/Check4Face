def ResizeImages(nombrecarpeta):
    for contador in range(10):
        imagen=Image.open(nombrecarpeta/+str(contador))

ResizeImages(blarep_main_top)


def convertirImagenAArchivo(nombreImagen, nombreDestino):
    imagen = Image.open(nombreImagen)
    imagen = imagen.convert('RGB')
    matrizNumpy = numpy.array(imagen)
    archivo = open(nombreDestino, 'w')
    for fila in matrizNumpy:
        for pixel in fila :
            for componente in pixel :
                archivo.write(' ' + str(componente))
            archivo.write(',')
        archivo.write('\n')
    archivo.close()
    return True

def leerArchivo(nombreEntrada):
    archivo = open(nombreEntrada,'r')
    matriz = []
    for i in archivo:
        lista = []
        fila = []
        lista = i.strip(",\n").split(',')
        for pixel in lista :
            aux = pixel.split()
            for e in range(3) :
                aux[e] = int(aux[e])
            fila.append(aux)
        matriz.append(fila)
    return matriz #matriz de la forma [[rojo,verde,azul],[rojo,verde,azul]]


def a-1o1(matriz):
    matriz_final=[]
    for linea in matriz:
       i = 0
       while i < len(linea):
           gris = (linea[i].sum())/3
           if gris<255/2:
               matriz_final.append(-1)
           else:
               matriz_final.append(1)
           i+=1
    return matriz
