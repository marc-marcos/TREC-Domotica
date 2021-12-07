# <3

import socket, jsonHandling, threading, pyfirmata, time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 420)) # locahost
sock.listen(1) # only one connection at the same time
connections = []

puerto = 'COM3'
tarjeta = pyfirmata.ArduinoMega(puerto)

pin1_0 = 34
pin1_1 = 28
pin1_2 = 27
pin1_3 = 31

pin2_0 = 30
pin2_1 = 26

pin3_0 = 36
pin3_1 = 22

pin4_0 = 32

pinExt1 = 42
pinExt2 = 43
pinExt3 = 44
pinExt4 = 45

pinLDR = 15
pinExtLDR = 0

buzz_pin = tarjeta.get_pin('d:9:p')
detectorPin = 0
timbrePin = tarjeta.digital[51]
# timbrePin.mode = pyfirmata.INPUT

it = pyfirmata.util.Iterator(tarjeta)
it.start()


tarjeta.analog[pinLDR].enable_reporting()

def handler(c, a):
    global connections

    while True:
        data = c.recv(1024)
        decodedData = data.decode()

        if decodedData == 'turnOn1':
            tarjeta.digital[pin1_0].write(1)
            tarjeta.digital[pin1_1].write(1)
            tarjeta.digital[pin1_2].write(1)
            tarjeta.digital[pin1_3].write(1)
            print("funciona")
        
        if decodedData == 'turnOff1':
            tarjeta.digital[pin1_0].write(0)
            tarjeta.digital[pin1_1].write(0)
            tarjeta.digital[pin1_2].write(0)
            tarjeta.digital[pin1_3].write(0)


        if decodedData == 'turnOn2':
            tarjeta.digital[pin2_0].write(1)
            tarjeta.digital[pin2_1].write(1)
        
        if decodedData == 'turnOff2':
            tarjeta.digital[pin2_0].write(0)
            tarjeta.digital[pin2_1].write(0)
        
        if decodedData == 'turnOn3':
            tarjeta.digital[pin3_0].write(1)
            tarjeta.digital[pin3_1].write(1)
        
        if decodedData == 'turnOff3':
            tarjeta.digital[pin3_0].write(0)
            tarjeta.digital[pin3_1].write(0)

        if decodedData == 'turnOn4':
            tarjeta.digital[pin4_0].write(1)

        if decodedData == 'turnOff4':
            tarjeta.digital[pin4_0].write(0)
        

        if decodedData == 'turnOnAuto':
            jsonHandling.writeData('serverCalls.json', 'autoMode', True)
        
        if decodedData == 'turnOffAuto':
            jsonHandling.writeData('serverCalls.json', 'autoMode', False)

        if decodedData == 'interiorAlarmOn':
            jsonHandling.writeData('serverCalls.json', 'interiorAlarm', True)

        if decodedData == 'interiorAlarmOff':
            jsonHandling.writeData('serverCalls.json', 'interiorAlarm', False)

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
                if float(input) > 0.4:
                    tarjeta.digital[pin1_0].write(1)
                    tarjeta.digital[pin1_1].write(1)
                    tarjeta.digital[pin1_2].write(1)
                    tarjeta.digital[pin1_3].write(1)
                    tarjeta.digital[pin2_0].write(1)
                    tarjeta.digital[pin2_1].write(1)
                    tarjeta.digital[pin3_0].write(1)
                    tarjeta.digital[pin3_1].write(1)
                    tarjeta.digital[pin4_0].write(1)
                    
                else:
                    tarjeta.digital[pin1_0].write(0)
                    tarjeta.digital[pin1_1].write(0)
                    tarjeta.digital[pin1_2].write(0)
                    tarjeta.digital[pin1_3].write(0)
                    tarjeta.digital[pin2_0].write(0)
                    tarjeta.digital[pin2_1].write(0)
                    tarjeta.digital[pin3_0].write(0)
                    tarjeta.digital[pin3_1].write(0)
                    tarjeta.digital[pin4_0].write(0)

        # ALARM SYSTEM
        if jsonHandling.readData('serverCalls.json', 'interiorAlarm') == 1:
            iterator = pyfirmata.util.Iterator(tarjeta)
            iterator.start()

            input = tarjeta.digital[detectorPin].read()

            if input == 1:
                threading.Thread(target = alarma).start()

        # TIMBRE
        it = pyfirmata.util.Iterator(tarjeta)
        it.start()

        tarjeta.digital[51].mode = pyfirmata.INPUT
        tarjeta.digital[8].mode = pyfirmata.OUTPUT
        tarjeta.digital[51].enable_reporting()

        if timbrePin.read():
            print('timbre')
            buzz_pin.write(0.6)
            time.sleep(0.2)
            
        
        else:
            buzz_pin.write(0)
            time.sleep(0.2)
        

def alarma():
    buzz_pin.write(0.6)
    time.sleep(1)
    buzz_pin.write(0)
    time.sleep(1)

# LOOP THREADS

threading.Thread(target = handleServer).start()
threading.Thread(target = arduino).start()