"""This file contains functions to abstract away sending and receiving
messages when building a server and client app using socket.

The function load_settings() will need to be called to load in settings from
a default filepath called "app_setup.pkl" belonging in the same directory as
the server.py and client.py.
"""
import os
import pickle

# server settings, use load_settings() to automatically set these variables.
HEADER = ''
FORMAT = ''
KEYWORDS = {}
PORT = 5050
SERVER = ''
ADDR = (SERVER, PORT)
MAX_RECV = 4096

def send_msg(conn, msg: str) -> bytes:
    """Encodes and sends a message to the socket connection.
    
    Args:
        conn: A socket connection.
        msg: A str message to be encoded.
        
    Returns:
        None, sends an encoded message to the socket connection.
    """
    message = msg.encode(FORMAT)
    send_len = str(len(message)).encode(FORMAT)
    # add padding to length of message
    send_len += b' ' * (HEADER - len(send_len))
    conn.send(send_len + message)

def recv_msg(conn) -> str:
    """Receives and decodes a message.
    
    Args:
        conn: A socket connection.

    Returns:
        A string message received from a socket connection.
    """
    # get length of message from bytes
    msg_len = conn.recv(HEADER).decode(FORMAT)
    msg_len = int(msg_len)
    
    # no message sent, return blank str
    if not msg_len:
        return ''
    
    # message length is within max buffer size
    if msg_len <= MAX_RECV:
        # receive rest of message
        return conn.recv(msg_len).decode(FORMAT)
    
    # message length exceeeds max buffer size
    result = []
    data_streaming = True
    stream_size = MAX_RECV
    print(msg_len)
    # stream data in chunks
    while data_streaming:
        # add msg to result
        result.append(conn.recv(stream_size).decode(FORMAT))
        msg_len -= stream_size # tracks remaining bytes
        print(msg_len)
        if msg_len < stream_size:
            stream_size = msg_len
        # exit loop after data streaming is completed.
        if not msg_len:
            data_streaming = False
            print('done streaming')
            return ''.join(result)

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
    global HEADER, FORMAT, KEYWORDS, PORT,\
    SERVER, ADDR, KEYWORDS, MAX_RECV
    # get directory path
    dir_path = os.path.split(filepath)[0]
    if not dir_path:
        dir_path = '.'
    # check if file exists
    if filepath in os.listdir(dir_path):
        with open(filepath, 'rb') as f:
            settings = pickle.load(f)
    else:
        print(f'No such file {filepath}.')
    
    # store into global variable
    HEADER = settings['header']
    FORMAT = settings['format']
    KEYWORDS = settings['keywords']
    PORT = settings['port']
    SERVER = settings['server']
    ADDR = (SERVER, PORT)
    MAX_RECV = settings['max_recv']
    
    return {
        'header': HEADER,
        'format': FORMAT,
        'keywords': KEYWORDS,
        'port': PORT,
        'server': SERVER,
        'addr': ADDR,
        'max_recv': MAX_RECV,
    }