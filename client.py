import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.226', 420))

while True:
    string_data = input('>>>')
    if string_data == 'exit':
        break

    else:
        s.send(bytes(string_data, encoding='utf8'))
