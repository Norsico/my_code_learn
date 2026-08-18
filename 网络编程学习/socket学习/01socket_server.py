import socket


server = socket.socket()

server.bind(('localhost', 8080))

server.listen(5)
count = 0
try:
    while True:
        client, client_info = server.accept()
        while True:
            data = client.recv(1024)
            print(data)
            print('-' * 23)
            if not data:
                count+=1
                print("Exit")
                print(f"count: {count}")
                break

except KeyboardInterrupt:
    pass