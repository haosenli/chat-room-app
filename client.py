from socket import socket
import socket as sock
import pickle
import sys
import threading

import data_transfer as dt

# load app settings
SETTINGS = dt.load_settings()
KEYWORDS = SETTINGS['keywords']
        
def log_in(client: socket):
    """Handles the log in procedure to a server.
    
    Args:
        client: A socket connection to a server.
        
    Returns:
        None.
    """
    d_type = dt.recv_data(client)[0]
    # handle banned user
    if d_type == KEYWORDS['banned']:
        print('[BANNED] You are banned from accessing this server.')
        sys.exit(0)
    # handle new user
    elif d_type == KEYWORDS['new_user']:
        name = input('Please enter your username: ')
        dt.send_data(client, name, KEYWORDS['user_cred'])
        d_type = dt.recv_data(client)[0]
        if d_type == KEYWORDS['success']:
            print('[NEW USER] Welcome to the server.')
        else:
            print('[ERROR] Connection to the server failed, please try again.')
            sys.exit(0)
    # handle user accept
    d_type, online = dt.recv_data(client)
    if d_type == KEYWORDS['success']:
        print(f'[CONNECTION] Welcome, there are {online} other users online.')
    else:
        print('[ERROR] Connection to the server failed, please try again.')
        sys.exit(0)

def client_receive(client: socket) -> None:
    """Receives data from server.

    Args: 
        client: A socket connection to the server.
    
    Returns:
        None.
    """
    connected = True
    while connected:
        d_type, msg = dt.recv_data(client)
        if d_type == KEYWORDS['disconnect']:
            connected = False
        elif d_type == KEYWORDS['text']:
            print(msg)
    # end thread
    sys.exit(0)
            
    
def client_send(client: socket) -> None:
    """Handles sending data to the server.
    
    Args:
        client: A socket connection to the server.
        
    Returns:
        None.
    """
    connected = True
    while connected:
        msg = input()
        # disconnect message
        if msg == KEYWORDS['disconnect']:
            dt.send_data(client, '', KEYWORDS['disconnect'])
            connected = False
        # text
        else:
            dt.send_data(client, msg, KEYWORDS['text'])
    # end thread
    sys.exit(0)

def run_program(client: socket) -> None:
    # wait for server authentication
    log_in(client)
    receive_handler = threading.Thread(target=client_receive, args=([client]))
    send_handler = threading.Thread(target=client_send, args=([client]))
    receive_handler.start()
    send_handler.start()

def connect() -> socket:
    """Connects to a server and returns the socket connection.
    
    Args:
        None.
        
    Returns:
        A socket connection to a server
    """
    # create client
    client = socket(sock.AF_INET, sock.SOCK_STREAM)
    # load in local server settings
    if SETTINGS['local']:
        try:
            client.connect((SETTINGS['local_ip'], SETTINGS['port']))
        except:
            # error message
            print(f'[ERROR] Please provide the local-ip address for'
                ' your local server in app_setup.py.')
            sys.exit(0)
    else:
        client.connect(SETTINGS['addr'])
    return client


def main():
    client = connect()
    run_program(client)

if __name__ == '__main__':
    main()