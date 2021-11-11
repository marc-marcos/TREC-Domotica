import socket, threading, time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 420))
sock.listen(1)
connections = []

def handler(c, a):
    global connections

    while True:
        data = c.recv(1024)
        decodedData = data.decode()

        print(decodedData)

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

threading.Thread(target = handleServer).start()