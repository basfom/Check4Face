from socket import socket
def main():
    s = socket()
    s.connect(("basfo", 6969))

    s.send("imagen")

    while True:
        f = open("5.jpg", "rb")
        content = f.read(1024)

        while content:
            # Enviar contenido.
            s.send(content)
            content = f.read(1024)
        break
    # Cerrar conexion y archivo.
    s.close()
    f.close()
    print("El archivo ha sido enviado correctamente.")

if __name__ == "__main__":
    main()
