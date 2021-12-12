import serial, time, socket, jsonHandling, threading, pandas, datetime # Importem totes les lliberires
# serial -> per establir la comunicació serie entre Arduino i Python
# time -> per poder esperar certs intervals de temps
# socket -> pel servidor web
# jsonHandling -> per modificar els arxius JSON, aquesta es una llibreria escrita integrament per mi
# threading -> per poder fer tasques en paralel
# pandas -> per poder exportar les dades de temperatura i llum com a format .xlsx (Excel)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Iniciem el servidor web
sock.bind(('0.0.0.0', 420))
sock.listen(1)
connections = []

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
            print('testing')
        
        elif decodedData == 'turnOff1':
            arduino.write(b'2')
        
        elif decodedData == 'turnOn2':
            arduino.write(b'3')
        
        elif decodedData == 'turnOff2':
            arduino.write(b'4')
        
        elif decodedData == 'turnOn3':
            arduino.write(b'5')
        
        elif decodedData == 'turnOff3':
            arduino.write(b'6')
        
        elif decodedData == 'turnOn4':
            arduino.write(b'7')
        
        elif decodedData == 'turnOff4':
            arduino.write(b'8')
        
        elif decodedData == 'onFogon':
            arduino.write(b'b')
        
        elif decodedData == 'offFogon':
            arduino.write(b'c')
        
        elif decodedData == 'turnOnAuto':
            jsonHandling.writeData('ServerCalls.json', 'autoMode', True)
            print('true')
        
        elif decodedData == 'turnOffAuto':
            jsonHandling.writeData('ServerCalls.json', 'autoMode', False)
            print('false')
        
        else:
            time = datetime.datetime.now()
            arduino.write(f'{time.hour}:{time.minute}')

        


def handleServer():  # Aquesta funció serveix per gestionar les peticions a més baix nivell, es a dir rep les peticions i per cada petició que rep crea un nou "fil" per tal de que les peticions es processin el més ràpid possible.
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
        # print(cleanStr)

        try: # Aqui utilitzem el mètode try perquè hi ha vegades que les primeres connexions amb Arduino no retornen totes les variables i amb l'estructura try/except podem veure aquest errors sense que detinguin el programa.
            interiorLDR, temperature, distanceAlarm = cleanStr.split("/")
                
            if jsonHandling.readData('serverCalls.json', 'autoMode') == 1: # Aquest if comproba al fitxer .json anterior si el mode automàtic està encès i en cas de que ho estigui comproba si la llum es superior a 700 i en aquest cas encen totes les llums. Si som completament corosos s'hauria de dir que el que mesurem es realment el nivell de foscor i no el nivell de llum, per tant si el LDR detecta més de 700/1023 de foscor encen totes les llums.

                if interiorLDR != None:
                    print(interiorLDR)
                    if int(interiorLDR) > 700:
                        arduino.write(b'9')
                                
                    else:
                        arduino.write(b'0')
                    
            if jsonHandling.readData('serverCalls.json', 'alarm') == 1: # Aquest if fa el mateix que el del LDR per amb l'alarma, llavors si detecta presencia a menys de 20cm fa que soni la alarma.

                print(distanceAlarm)
                if int(distanceAlarm) < 20:
                    arduino.write(b'a')
                    jsonHandling.writeData('serverCalls.json', 'alarm', 0)
            
            df = df.append({"Temperatura":float(temperature), "Light Level":int(interiorLDR)}, ignore_index=True)
            # print(df)

            i += 1 # Cada vegada que aquest loop fa una volta li sumem 1 a i i quan i es multiple de 30 (més o menys cada 30 segons), agafem tots els valors de temperatura i llum i els guardem a excel.xlsx .


            if i % 10 == 0:
                df.to_excel('excel.xlsx')

                
        except Exception as e: # En cas de detectar un error l'imprimim per tal de que sigui més facil d'identificar-lo.
            print(e)
     
threading.Thread(target = handleServer).start() # Encenem la funció que s'encarrega del servidor.
threading.Thread(target = getIterators).start() # Encenem la funció que s'encarrega dels iteradors.