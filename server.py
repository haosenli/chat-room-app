"""This program runs the Python server back-end of a chat room application.
"""
from socket import socket
import socket as sock
import threading
import sys
from typing import Any

from utils.connection_manager import ConnectionManager
from utils.user import User
import data_transfer as dt

# load app settings
SETTINGS = dt.load_settings()
KEYWORDS = SETTINGS['keywords']

def client_auth(conn: socket, ip: str) -> None:
    """Handles client authentication.
    
    Args:
        conn: A socket connection of a client.
    
    Returns:
        None.
    """
    # check if user exists in server list
    # user is banned, send ban msg and close connection
    if CONNECTIONS.contains_user(ip) == -1:
        dt.send_data(conn, '', KEYWORDS['banned'])
        conn.close()
        print(f'[CONNECTION] Banned {ip} tried to connect.')
        
    # user is new, create user profile
    elif CONNECTIONS.contains_user(ip) == 0:
        # edit to use keywords
        dt.send_data(conn, '', KEYWORDS['new_user'])
        rdata = dt.recv_data(conn)
        if rdata[0] == KEYWORDS['user_cred']:
            # construct User object and add to server
            user = User(rdata[1], ip, conn)
            CONNECTIONS.add_user(user)
            print(f'[NEW USER] New user {user.get_username()} ' + \
                f'connected from {user.get_ip()}!')
            dt.send_data(conn, '', KEYWORDS['success'])
        else:
            # connection failed, try again.
            dt.send_data(conn, '', KEYWORDS['conn_error'])
            conn.close()
            
    # authorize user
    dt.send_data(conn, f'{threading.active_count()-2}', KEYWORDS['success'])
    user = CONNECTIONS.online_user(ip)
    user.set_socket(conn)
    print(f'[CONNECTION] User {user.get_username()} successfully connected.')
    msg_all(user, 
            f'{user.get_username()} connected to the server!', 
            KEYWORDS['text'])
        
def msg_all(user: User, content: Any, d_type: str) -> None:
    """Messages all users in the server chat room, except for the sender.
    
    Args:
        user: A User representing the sender.
        content: Any content the user is sending.
        d_type: A str indicating the datatype of the content.
        
    Returns:
        None.
    """
    recipients = CONNECTIONS.non_senders(user.get_ip())
    print(f"[SENDING] Sending {user.get_username()}'s message to " +\
        f"{len(recipients)} other users.")
    for recipient in recipients:
        data = f'{user.get_username()}: {content}'
        dt.send_data(recipient.get_socket(), data, d_type)
        print(f'   > Sent message to {recipient.get_username()}')

def handle_client(conn: socket, addr: str) -> None:
    """Handles client connections.
    
    Args:
        conn: A socket connection of a client.
        addr: An address of a client.
        
    Returns:
        None.
    """
    # authenticate user
    ip = addr[0]
    client_auth(conn, ip)
    user = CONNECTIONS.get_user(ip)
    # wait to receive from client
    while CONNECTIONS.is_online(ip):
        # while connected:
        print('[STATUS] Waiting to recieve data.')
        d_type, rdata = dt.recv_data(conn)
        print(f'[RECEIVED] {user.get_username()} sent a {d_type}.')
        
        # disconnect keyword
        if d_type == KEYWORDS['disconnect']:
            CONNECTIONS.offline_user(ip)
            dt.send_data(conn, '', KEYWORDS['disconnect'])
            print(f'[DISCONNECT] {user.get_username()} disconnected.')
            
        # send message to other users
        if d_type == KEYWORDS['text']:
            msg_all(user, rdata, d_type)
        
    # close client connection
    print(f'[CLOSED CONNECTION] {user.get_username()} disconnected.')
    conn.close()
    sys.exit(0)
    
def server_start() -> None:
    """Starts the server.
    
    Creates a thread for each client connection.
    
    Args:
        None.
    
    Returns:
        None.    
    """
    global SERVER
    SERVER.listen()
    print(f'[STATUS] Server is listenting on {SETTINGS["server"]}')
    while True:
        conn, addr = SERVER.accept()
        # create new thread for each client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.active_count()-1}')

# create server
SERVER = socket(sock.AF_INET, sock.SOCK_STREAM)
SERVER.bind(SETTINGS['addr'])

# server manager
CONNECTIONS = ConnectionManager()


def main():
    print('[STATUS] server is starting...')
    server_start()

if __name__ == '__main__':
    main()