"""This program runs the Python server back-end of a chat room application.
"""
import threading
import socket
import pickle

# encoding
HEADER = 64
FORMAT = 'utf-8'

# server setup
PORT = 5678
SERVER = '173.230.158.55'
ADDR = (SERVER, PORT)
DISCONNECT_MSG = '!exit'

# create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr) -> None:
    """Handles client connections.
    
    Args:
        client: A tuple of socket object and address representing the client.
        This is the return value of socket.accept() function.
        
    Returns:
        None.
    """
    print(f'[NEW CONNECTION] {addr} connected.')
    # wait to receive from client
    connected = True
    while connected:
        # parse header to find length of message
        msg_len = conn.recv(HEADER).decode(FORMAT)
        # ignore if no content was sent
        if msg_len:
            msg_len = int(msg_len)
            # receive rest of message
            msg = conn.recv(msg_len).decode(FORMAT)
            # check if user wishes to disconnect
            if msg == DISCONNECT_MSG:
                connected = False
            print(f'[{addr}] {msg}')
    # close client connection
    print(f'[CLOSED CONNECTION] {addr} disconnected.')
    conn.close()
    
def server_start() -> None:
    """Starts the server.
    
    Creates a thread for each client connection.
    
    Args:
        None.
    
    Returns:
        None.    
    """
    server.listen()
    print(f'[LISTENING] Server is listenting on {SERVER}')
    while True:
        conn, addr = server.accept()
        # create new thread for each client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount()-1}')


def main():
    print('[STARTING] server is starting...')
    server_start()

if __name__ == '__main__':
    main()