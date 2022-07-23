"""Sets up server information and encoding protocol.

Run this script to generate a new setup file for the socket application.

*To run this on a server with a public IP address:
- Edit the 'server' value to the Public IP address of your server
- Edit the 'local' value to be False.
- Rest are optional.

*To run this locally on a private IP address (DEFUALT):
- Set 'server' to be an empty str.
- Set 'local' to be True.
- Set 'local-ip' to the local server's IP address.
- Rest are optional.

Example usage:
    > python3 app_setup.py
    > [COMPLETE] Succesfully updated app setup info.
"""
import pickle


# filepath
filepath = 'app_setup.pkl'

# protocol setup
protocol = {
    'server': '', # server ip address
    'local': True,
    'local_ip': '', # local server ip (i.e. 192.168.0...)
    'port': 5678, # port number
    'header': 64, # header
    'format': 'utf-8', # encoding
    'keywords': { # keyword messages
        'disconnect': '!exit'
        }, 
    'max_recv': 4096,
}

with open(filepath, 'wb') as f:
    pickle.dump(protocol, f, pickle.HIGHEST_PROTOCOL)

print('[COMPLETE] Succesfully updated app setup info.')