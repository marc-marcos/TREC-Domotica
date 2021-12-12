import serial, time, socket, jsonHandling, threading, pandas # Importem totes les llibreries necessaries.

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind(('0.0.0.0', 420))
sock.listen(1)
connections = [] # Inicialitzem el servidor a l'amfitrió local.

f = open('filekey.key', 'r') # Obrim el fitxer on s'emmagatzema la clau de xifratge
code = f.readline() # I la guardem en una variable amb la que la llibreria socket automaticament la desxifrará
f.close()

puerto = 'COM3'
arduino = serial.Serial(puerto, 9600)
time.sleep(2) # Definim a quin port està conectat l'Arduino i esperem 2 segons per tal de que s'efectui la connexió.

def handler(c, a): # Aquesta es la funció que rep les peticions de la aplicació, les desxifra i les passa a Arduino.
    global connections

    while True:
        data = c.recv(1024) # Li diem a Python que com a molt accepte 1024 bytes de petició (més que suficient)
        decodedData = data.decode()

        if decodedData == 'turnOn1': # Tota la llista de comands que volem que Python sigui capaç d'enviar-li a Arduino
            arduino.write(b'1')
        
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
        
        if decodedData == 'onFogon':
            arduino.write(b'b')
        
        if decodedData == 'offFogon':
            arduino.write(b'c')
        
        if decodedData == 'turnOnAuto':
            jsonHandling.writeData('ServerCalls.json', 'autoMode', True) # Aquests dos comands son importants perquè a més de enviar-li el comand a Python escriuen si el mode automàtic està encès o no a un fitxer .json. Això ho faig perquè necessito saber si el mode automàtic està encès desde una funció que funciona paralelament a la que rep les peticions.
            print('true')
        
        if decodedData == 'turnOffAuto':
            jsonHandling.writeData('ServerCalls.json', 'autoMode', False)
            print('false') 

        if decodedData == 'turnAlarmaOn':
            jsonHandling.writeData('ServerCalls.json', 'alarm', True) # Fem el mateix amb el json de la alarma que amb el json del LDR, quan cambiem l'estat de l'alarma ho escribim al fitxer json.
        
        if decodedData == 'turnAlarmaOff':
            jsonHandling.writeData('ServerCalls.json', 'alarm', False)

def handleServer(): # Aquesta funció serveix per gestionar les peticions a més baix nivell, es a dir rep les peticions i per cada petició que rep crea un nou "fil" per tal de que les peticions es processin el més ràpid possible.
    while True:
        c, a = sock.accept()
        cThread = threading.Thread(target=handler, args=(c, a))
        cThread.daemon = True
        cThread.start()
        connections.append(c) 
        #print(connections)

def getIterators(): # Aquesta funció s'encarrega de totes les coses que tenen a veure amb els iteradors. Això és la alarma, el LDR i per tant el mode automàtic i la temperatura.
    df = pandas.DataFrame(columns = ["Temperatura", "Light Level"])
    i = 0

    while True:

        cleanStr = arduino.readline().decode('utf-8') # Rebem totes les dades per connexió serie i les pasem a format utf-8.

        try: # Aqui utilitzem el mètode try perquè hi ha vegades que les primeres connexions amb Arduino no retornen totes les variables i amb l'estructura try/except podem veure aquest errors sense que detinguin el programa.
            interiorLDR, distanceAlarm, temperature = cleanStr.split("/")
                
            if jsonHandling.readData('serverCalls.json', 'autoMode') == 1: # Aquest if comproba al fitxer .json anterior si el mode automàtic està encès i en cas de que ho estigui comproba si la llum es superior a 700 i en aquest cas encen totes les llums. Si som completament corosos s'hauria de dir que el que mesurem es realment el nivell de foscor i no el nivell de llum, per tant si el LDR detecta més de 700/1023 de foscor encen totes les llums.
                if interiorLDR != None:
                    print(interiorLDR)
                    if int(interiorLDR) > 700:
                        arduino.write(b'9')
                                
                    else:
                        arduino.write(b'0')
                    
            if jsonHandling.readData('serverCalls.json', 'alarm') == 1: # Aquest if fa el mateix que el del LDR per amb l'alarma, llavors si detecta presencia a menys de 20cm fa que soni la alarma.
                if int(distanceAlarm) < 20:
                    arduino.write(b'a')

            i += 1 # Cada vegada que aquest loop fa una volta li sumem 1 a i i quan i es multiple de 30 (més o menys cada 30 segons), agafem tots els valors de temperatura i llum i els guardem a excel.xlsx .
            
            if i % 30 == 0:
                df = df.append({"Temperatura":float(temperature), "Light Level":int(interiorLDR)}, ignore_index=True)
                df.to_excel('excel.xlsx')
                # print('excel report generated')

                
        except Exception as e: # En cas de detectar un error l'imprimim per tal de que sigui més facil d'identificar-lo.
            print(e)
    
threading.Thread(target = handleServer).start() # Encenem la funció que s'encarrega del servidor.
threading.Thread(target = getIterators).start() # Encenem la funció que s'encarrega dels iteradors.