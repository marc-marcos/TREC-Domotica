# <3

import socket, jsonHandling, threading, pyfirmata, time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 420)) # locahost
sock.listen(1) # only one connection at the same time
connections = []

pin1 = 50
pin2 = 52
pin3 = 54

pinExt1 = 42
pinExt2 = 43
pinExt3 = 44
pinExt4 = 45

pinLDR = 8
pinExtLDR = 0

piezoPin = 0 # tiene que ser pwm
detectorPin = 0
timbrePin = 0

puerto = 'COM3'
tarjeta = pyfirmata.ArduinoMega(puerto)

it = pyfirmata.util.Iterator(tarjeta)
it.start()

tarjeta.analog[pinLDR].enable_reporting()
tarjeta.digital[detectorPin].enable_reporting()

def handler(c, a):
    global connections

    while True:
        data = c.recv(1024)
        decodedData = data.decode()

        if decodedData == 'toggle1':
            toggle = jsonHandling.readData('serverCalls.json', 'led1')
            if toggle:
                jsonHandling.writeData('serverCalls.json', 'led1', False)
                tarjeta.digital[pin1].write(0)
            else:
                jsonHandling.writeData('serverCalls.json', 'led1', True)
                tarjeta.digital[pin1].write(1)
        
        if decodedData == 'toggle2':
            toggle = jsonHandling.readData('serverCalls.json', 'led2')
            if toggle:
                jsonHandling.writeData('serverCalls.json', 'led2', False)
                tarjeta.digital[pin2].write(0)
            else:
                jsonHandling.writeData('serverCalls.json', 'led2', True)
                tarjeta.digital[pin2].write(1)

        if decodedData == 'toggle3':
            toggle = jsonHandling.readData('serverCalls.json', 'led3')
            if toggle:
                jsonHandling.writeData('serverCalls.json', 'led3', False)
                tarjeta.digital[pin3].write(0)
            else:
                jsonHandling.writeData('serverCalls.json', 'led3', True)
                tarjeta.digital[pin3].write(1)
        
        if decodedData == 'outsideAutoMode':
            toggle = jsonHandling.readData('serverCalls.json', 'outsideAutoMode')
            if toggle:
                jsonHandling.writeData('serverCalls.json', 'outsideAutoMode', False)
            else:
                jsonHandling.writeData('serverCalls.json', 'outsideAutoMode', True)
        
        if decodedData == 'autoMode':
            toggle = jsonHandling.readData('serverCalls.json', 'autoMode')
            if toggle:
                jsonHandling.writeData('serverCalls.json', 'autoMode', False)
            else:
                jsonHandling.writeData('serverCalls.json', 'autoMode', True)

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

        # AUTO MODE AND EXTERIOR AUTO MODE
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
        
        if jsonHandling.readData('serverCalls.json', 'outsideAutoMode') == 1:
            if tarjeta.analog[pinExtLDR].read() != None:
                if float(input) < 0.3:
                    tarjeta.digital[pinExt1].write(1)
                    tarjeta.digital[pinExt2].write(1)
                    tarjeta.digital[pinExt3].write(1)
                    tarjeta.digital[pinExt4].write(1)
                
                else:
                    tarjeta.digital[pinExt1].write(0)
                    tarjeta.digital[pinExt2].write(0)
                    tarjeta.digital[pinExt3].write(0)
                    tarjeta.digital[pinExt4].write(0)

        # ALARM SYSTEM
        if jsonHandling.readData('serverCalls.json', 'alarmOn') == 1:
            iterator = pyfirmata.util.Iterator(board)
            iterator.start()

            input = tarjeta.digital[detectorPin].read()

            if input == 1:
                threading.Thread(target = alarma).start()

        time.sleep(0.1)

def alarma():
    tarjeta.digital[piezoPin].write(0.6)
    time.sleep(1)
    tarjeta.digital[piezoPin].write(0)
    time.sleep(1)

threading.Thread(target = handleServer).start()
threading.Thread(target = arduino).start()