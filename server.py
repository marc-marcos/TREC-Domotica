# <3

import socket, jsonHandling, threading, pyfirmata, time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 420)) # locahost
sock.listen(1) # only one connection at the same time
connections = []

pin1 = 50
pin2 = 52
pin3 = 54

pinLDR = 8

puerto = 'COM3'
tarjeta = pyfirmata.ArduinoMega(puerto)

it = pyfirmata.util.Iterator(tarjeta)
it.start()

tarjeta.analog[pinLDR].enable_reporting()

def handler(c, a):
    global connections

    while True:
        data = c.recv(1024)
        decodedData = data.decode()

        if decodedData == 'autoModeOn':
            jsonHandling.writeData('serverCalls.json', 'autoMode', 1) # AUTO MODE ON JSON

        if decodedData == 'autoModeOff':
            jsonHandling.writeData('serverCalls.json', 'autoMode', 0)
        
        if decodedData == 'turnOn1':
            tarjeta.digital[pin1].write(1) # LED 1
        
        if decodedData == 'turnOff1':
            tarjeta.digital[pin1].write(0)
        
        if decodedData == 'turnOn2':
            tarjeta.digital[pin2].write(1) # LED 2
        
        if decodedData == 'turnOff2':
            tarjeta.digital[pin2].write(0)
        
        if decodedData == 'turnOn3':
            tarjeta.digital[pin3].write(1) # LED 3
        
        if decodedData == 'turnOff3':
            tarjeta.digital[pin3].write(0)

        if not data:
            connections.remove(c)
            c.close()
            break

def handleServer():
    while True:
        c, a = sock.accept()
        cThread = threading.Thread(target=handler, args=(c, a))
        cThread.daemon = True
        cThread.start()
        connections.append(c)
        #print(connections)

def arduino():
    while True:
        if jsonHandling.readData('serverCalls.json', 'autoMode') == 1:
            input = tarjeta.analog[pinLDR].read()
            print(input)

            if input != None:
                if float(input) < 0.3:
                    tarjeta.digital[pin1].write(1)
                    tarjeta.digital[pin2].write(1)
                    
                else:
                    tarjeta.digital[pin1].write(0)
                    tarjeta.digital[pin2].write(0)
        
        time.sleep(0.1)

threading.Thread(target = handleServer).start()
threading.Thread(target = arduino).start()