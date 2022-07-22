import socket
import pickle


# encoding
HEADER = 64
FORMAT = 'utf-8'

# server info
PORT = 5678
SERVER = '173.230.158.55' # ip address
ADDR = (SERVER, PORT)
DISCONNECT_MSG = '!exit'

# create client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    send_len = str(len(message)).encode(FORMAT)
    # add padding to length of message
    send_len += b' ' * (HEADER - len(send_len))
    # send byte content
    client.send(send_len)
    client.send(message)
    
connected = True
while connected:
    usr_input = input('Message: ')
    if usr_input == DISCONNECT_MSG:
        send(DISCONNECT_MSG)
        break
    send(usr_input)
    