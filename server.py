# <3

import socket
import threading
import pyfirmata

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('0.0.0.0', 420))
sock.listen(1)
connections = []

pin1 = (2)
pin2 = (3)
pin3 = (4)
puerto = "/dev/ttyACM0"
tarjeta = pyfirmata.ArduinoMega(puerto)


def handler(c, a):
    global connections

    while True:
        data = c.recv(1024)
        decodedData = data.decode()

        if decodedData == 'turnOn1':
            tarjeta.digital[pin1].write(1)

        if decodedData == 'turnOff1':
            tarjeta.digital[pin1].write(0)
        
        if decodedData == 'turnOn2':
            tarjeta.digital[pin2].write(1)

        if decodedData == 'turnOff2':
            tarjeta.digital[pin2].write(0)

        if decodedData == 'turnOn3':
            tarjeta.digital[pin3].write(1)
        
        if decodedData == 'turnOff3':
            tarjeta.digital[pin3].write(0)

        if not data:
            connections.remove(c)
            c.close()
            break

        print(decodedData)

while True:
    c, a = sock.accept()
    cThread = threading.Thread(target=handler, args=(c, a))
    cThread.daemon = True
    cThread.start()
    connections.append(c)
    #print(connections)
