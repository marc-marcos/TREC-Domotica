import serial, time, socket, jsonHandling, threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 420))
sock.listen(1)
connections = []

puerto = 'COM3'
arduino = serial.Serial(puerto, 9600)
time.sleep(2)

def handler(c, a):
    global connections

    while True:
        data = c.recv(1024)
        decodedData = data.decode()

        if decodedData == 'turnOn1':
            arduino.write(b'1')
            print('testing')
        
        if decodedData == 'turnOff1':
            arduino.write(b'2')
        
        if decodedData == 'turnOn2':
            arduino.write(b'3')
        
        if decodedData == 'turnOff2':
            arduino.write(b'4')
        
        if decodedData == 'turnOn3':
            arduino.write(b'5')
        
        if decodedData == 'turnOff3':
            arduino.write(b'6')
        
        if decodedData == 'turnOn4':
            arduino.write(b'7')
        
        if decodedData == 'turnOff4':
            arduino.write(b'8')
        
        if decodedData == 'turnOnAuto':
            jsonHandling.writeData('ServerCalls.json', 'autoMode', True)
            print('true')
        
        if decodedData == 'turnOffAuto':
            jsonHandling.writeData('ServerCalls.json', 'autoMode', False)
            print('false')


def handleServer():
    while True:
        c, a = sock.accept()
        cThread = threading.Thread(target=handler, args=(c, a))
        cThread.daemon = True
        cThread.start()
        connections.append(c)
        #print(connections)

def getIterators():
    while True:

        cleanStr = arduino.readline().decode('utf-8')
        # print(cleanStr)

        try:
            interiorLDR, distanceAlarm, temperature = cleanStr.split("/")
                
            if jsonHandling.readData('serverCalls.json', 'autoMode') == 1:
                if interiorLDR != None:
                    print(interiorLDR)
                    if int(interiorLDR) > 700:
                        arduino.write(b'9')
                                
                    else:
                        arduino.write(b'0')
                    
            if jsonHandling.readData('serverCalls.json', 'interiorAlarm') == 1:
                if int(distanceAlarm) < 20:
                    arduino.write(b'a')
            
        except:
            print('error')
    
threading.Thread(target = handleServer).start()
threading.Thread(target = getIterators).start()


# import serial, time

# arduino = serial.Serial("COM3", 9600)
# time.sleep(2)
# arduino.write(b'1')
# arduino.close()