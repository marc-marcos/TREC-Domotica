imort socket
import threading
import pyfirmata

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('0.0.0.0', 420))
sock.listen(1)
connections = []

pin = (24)
puerto = "\\.\ACM0"
tarjeta = pyfirmata.ArduinoMega(puerto)


def handler(c, a):
    global connections
    while True:
        data = c.recv(1024)
        decodedData = data.decode()

        if decodedData == 'encender':
            tarjeta.digital[pin].write(1)

        elif decodedData == 'apagar':
            tarjeta.digital[pin].write(0)

        if not data:
            connections.remove(c)
            c.close()
            break

while True:
    c, a = sock.accept()
    cThread = threading.Thread(target=handler, args=(c, a))
    cThread.daemon = True
    cThread.start()
    connections.append(c)
    print(connections)
