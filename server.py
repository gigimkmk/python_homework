import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = {}


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)

            username = usernames[client]

            broadcast(f"{username}: {message.decode()}".encode())

        except:
            clients.remove(client)

            username = usernames[client]
            del usernames[client]

            client.close()

            broadcast(f"{username} left the chat.".encode())
            break


def receive():
    while True:
        client, address = server.accept()

       
        username = client.recv(1024).decode()

        usernames[client] = username
        clients.append(client)

        print(f"{username} joined the chat.")

        broadcast(f"{username} joined the chat.".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server started...")
receive()