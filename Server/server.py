import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 6969))
s.listen(1)

sc, addr = s.accept()

file_flag = False

while True:

    #Recibimos el mensaje, con el metodo recv recibimos datos y como parametro
    #la cantidad de bytes para recibir
    recibido = sc.recv(1024)

    sc.send("hola")

    #Si el mensaje recibido es la palabra close se cierra la aplicacion
    if recibido == "close":
        break

    elif recibido == "entrenar":
        #Generar embeddings
        os.system("batch-represent/main.lua -outDir embeddings/ -data db/")
        os.system("classifier.py train embeddings")
        print "Neurona entrenada satisfactoriamente!"

    elif recibido == "comparar":
        pass
    #Si se reciben datos nos muestra la IP y el mensaje recibido
    print str(addr[0]) + " dice: ", recibido

    #Devolvemos el mensaje al cliente
    sc.send(recibido)
print "Adios."
