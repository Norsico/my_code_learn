import socket 

client = socket.socket()

client.connect(('localhost', 8080))

with open('./data.txt', 'rb') as f:
    while True:
        data = f.read(1024)
        client.send(data)
        if not data:
            break