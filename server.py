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
pinsList = (2, 3, 4)

pinAuto = (5)
puerto = "/dev/ttyACM0"
tarjeta = pyfirmata.ArduinoMega(puerto)

def turnAllOff(pins):
    for i in pins:
        tarjeta.digital[i].write(0)

def turnAllOn(pins):
    for i in pins:
        tarjeta.digital[i].write(1)

def handler(c, a):
    global connections

    while True:
        data = c.recv(1024)
        decodedData = data.decode()
        
        if decodedData == 'turnAllOff':
            turnAllOff(pinsList)

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

        if decodedData == 'turnOnAuto':
            tarjeta.digital[pinAuto].write(1)
            turnAllOff(pinsList)
            
        
        if decodedData == 'turnOffAuto':
            tarjeta.digital[pinAuto].write(0)
            turnAllOn(pinsList)

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
