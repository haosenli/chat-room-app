import socket
import pickle


import data_transfer as dt

# load app settings
SETTINGS = dt.load_settings()
KEYWORDS = SETTINGS['keywords']

# create client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SETTINGS['addr'])


def main():
    connected = True
    while connected:
        user_input = input('Message: ')
        if user_input == KEYWORDS['disconnect']:
            dt.send_msg(client, KEYWORDS['disconnect'])
            break
        dt.send_msg(client, user_input)


if __name__ == '__main__':
    main()