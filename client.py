import socket
import pickle
import sys

import data_transfer as dt

# load app settings
SETTINGS = dt.load_settings()
KEYWORDS = SETTINGS['keywords']
print(SETTINGS)

# create client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# load in local server settings
if SETTINGS['local']:
    try:
        client.connect((SETTINGS['local_ip'], SETTINGS['port']))
    except:
        ABORT = True
        # error message
        print(f'[ERROR] Please provide the local-ip address for'
            ' your local server in app_setup.py.')
else:
    client.connect(SETTINGS['addr'])


def main():
    global ABORT
    connected = True
    while connected and not ABORT: 
        user_input = input('Message: ')
        if user_input == KEYWORDS['disconnect']:
            dt.send_msg(client, KEYWORDS['disconnect'])
            break
        dt.send_msg(client, user_input)


if __name__ == '__main__':
    main()