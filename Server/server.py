import socket
import os
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 2213))
s.listen(1)

sc, addr = s.accept()

file_flag = False

while True:

    #Recibimos el mensaje, con el metodo recv recibimos datos y como parametro
    #la cantidad de bytes para recibir
    recibido = sc.recv(1024)

    #Si el mensaje recibido es la palabra close se cierra la aplicacion
    if recibido == "close":
        break

    elif recibido == "imagen":
        f = open("3.jpg", "wb")
        while True:
            try:
                # Recibir datos del cliente.
                time.sleep(2)
                input_data = sc.recv(1024)
            except socket.error:
                print("Error de lectura.")
                break
            else:
                if input_data:
                    f.write(input_data)
                else:
                    break

        print("El archivo se ha recibido correctamente.")
        f.close()

    elif recibido == "entrenar":
        #Generar embeddings
        os.system("../openface/batch-represent/main.lua -outDir info/ -data ../Client/db_neuronas/")
        os.system("../openface/demos/classifier.py train ./info/")
        print "Neurona entrenada satisfactoriamente!"

    elif recibido == "comparar":
        pass
    #Si se reciben datos nos muestra la IP y el mensaje recibido
    print str(addr[0]) + " dice: ", recibido

    #Devolvemos el mensaje al cliente
    #sc.send(recibido)
print "Adios."
