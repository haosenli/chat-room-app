"""This program runs the Python server back-end of a chat room application.
"""
import threading
import socket
import pickle
import os

from utils.connection_manager import ConnectionManager
from utils.user import User
import data_transfer as dt

# load app settings
SETTINGS = dt.load_settings()
KEYWORDS = SETTINGS['keywords']


def handle_client(conn, addr) -> None:
    """Handles client connections.
    
    Args:
        conn: A socket connection of a client.
        addr: An address of a client.
        
    Returns:
        None.
    """
    print(f'[NEW CONNECTION] {addr} connected.')
    # ip = addr[0]
    # # check if user exists in server list
    # # user is banned, send ban msg and refuse connection
    # if CONNECTIONS.contains_user(ip) == -1:
    #     dt.send_msg('You are banned from this server.')

    # # user is new, create user profile
    # if CONNECTIONS.contains_user(ip) == 0:
    #     # edit to use keywords
    #     dt.send_msg('Enter in your username.')
    #     username = dt.recv_msg(conn)
    #     # construct User object
    #     CONNECTIONS.add_user()
    
    # wait to receive from client
    connected = True
    while connected:
        msg = dt.recv_msg(conn)
        if msg == KEYWORDS['disconnect']:
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
    print(f'[LISTENING] Server is listenting on {SETTINGS["server"]}')
    while True:
        conn, addr = server.accept()
        # create new thread for each client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount()-1}')

# create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SETTINGS['addr'])

# server manager
# CONNECTIONS = ConnectionManager()


def main():
    print('[STARTING] server is starting...')
    server_start()

if __name__ == '__main__':
    main()