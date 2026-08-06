import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter your username: ")


client.send(username.encode())


def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("The server has been closed.")
            client.close()
            break


def write():
    while True:
        message = input()
        client.send(message.encode())


threading.Thread(target=receive).start()
threading.Thread(target=write).start()