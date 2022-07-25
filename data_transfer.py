"""This file contains functions to abstract away sending and receiving
messages when building a server and client app using socket.

The function load_settings() will need to be called to load in settings from
a default filepath called "app_setup.pkl" belonging in the same directory as
the server.py and client.py.
"""
import os
import pickle
from typing import Any
from socket import socket

# server settings, use load_settings() to automatically set these variables.
HEADER = ''
FORMAT = ''
KEYWORDS = {}
PORT = 5050
SERVER = ''
ADDR = (SERVER, PORT)
MAX_RECV = 4096
LOCAL = False
LOCAL_IP = ''

def send_data(connection: socket, data: Any, data_type: str=None) -> None:
    """Encodes and sends pickle'd data to the socket connection.
    
    Args:
        connection: A socket connection.
        data: Any pickle-able (serializable) data.
        data_type: An (optional) str indicating the type of message.
            Defaults to 'text' data.
        
    Returns:
        None, sends an encoded data to the socket connection.
    """
    msg_len = str(len(data)).encode(FORMAT)
    data_type = data_type.encode(FORMAT)
    # add padding to length of message
    msg_len += b' ' * (HEADER - len(msg_len))
    data_type += b' ' * (HEADER - len(data_type))
    connection.send(msg_len + data_type + data.encode(FORMAT))
    # connection.send(msg_len + data_type + pickle.dumps(data))
        
def recv_data(connection: socket) -> tuple[str, Any]:
    """Receives and decodes data.
    
    This is a blocking function.
    
    Args:
        connection: A socket connection.

    Returns:
        A tuple containing a str indicating data type of the content,
        and any type of content received from a socket connection.
    """
    # parse length of message and data type from received data
    msg_len = connection.recv(HEADER).decode(FORMAT).strip()
    data_type = connection.recv(HEADER).decode(FORMAT).strip()
    msg_len = int(msg_len)
    
    # no message sent, return blank str
    if not msg_len:
        return data_type, ''
    
    # message length is within max buffer size
    if msg_len <= MAX_RECV:
        data = connection.recv(msg_len).decode(FORMAT)
        return data_type, data
        # return data_type, pickle.loads(data)
    
    # message length exceeeds max buffer size
    data = []
    data_streaming = True
    stream_size = MAX_RECV
    # stream data in chunks
    while data_streaming:
        # add msg to result
        data.append(connection.recv(stream_size))
        msg_len -= stream_size # tracks remaining bytes
        if msg_len < stream_size:
            stream_size = msg_len
        # exit loop after data streaming is completed.
        if not msg_len:
            data_streaming = False
            return data_type, pickle.loads(b''.join(data))

def load_settings(filepath: str='app_setup.pkl') -> dict:
    """Sets up encoding and header formats automatically
    from a .pkl file generated from app_setup.py.
    
    Args:
        filepath: A (optional) str filepath containing the
            server information.
        
    Returns:
        A dict containing server settings information.
        Available keys are header, format, disconnect_msg,
        port, server, addr, max_recv.
    """
    global ADDR, SERVER, LOCAL, LOCAL_IP, PORT, \
        HEADER, FORMAT, KEYWORDS, MAX_RECV
    # get directory path
    dir_path = os.path.split(filepath)[0]
    if not dir_path:
        dir_path = '.'
    # check if file exists
    if filepath in os.listdir(dir_path):
        with open(filepath, 'rb') as f:
            settings = pickle.load(f)
    else:
        raise Exception(f'[ERROR] No such file "{filepath}".')
    
    # store into global variable
    SERVER = settings['server']
    LOCAL = settings['local']
    LOCAL_IP = settings['local_ip']
    PORT = settings['port']
    HEADER = settings['header']
    FORMAT = settings['format']
    KEYWORDS = settings['keywords']
    MAX_RECV = settings['max_recv']
    ADDR = (SERVER, PORT)
    
    return {
        'addr': ADDR,
        'server': SERVER,
        'local': LOCAL,
        'local_ip': LOCAL_IP,
        'port': PORT,
        'header': HEADER,
        'format': FORMAT,
        'keywords': KEYWORDS,
        'max_recv': MAX_RECV,
    }