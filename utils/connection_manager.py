"""This file contains the connectionManager class.
"""
import pickle           # file IO
import os               # file paths
from typing import IO   # typing


from utils.user import User   # custom class for users

class ConnectionManager:
    """ConnectionManager provides a runtime optimized interface
    for connected users in the chat room app.
    """
    def __init__(self) -> None:
        """Constructs a ConnectionManager object.
        """
        self.online_users = {} # stores currently online users by ip
        self.banned_users = {} # stores banned users by ip
        self.all_users = {} # stores all users by ip
        self.read_instance()
    
    def add_user(self, user: User) -> None:
        """Adds a new User to server list.
        
        Does nothing if the user is already in server list.
        
        Args:
            user: A User object.
            
        Returns:
            None.
        """
        if user.get_ip() in self.all_users:
            return
        self.all_users[user.get_ip()] = user
        
    def get_user(self, ip: str) -> User:
        """Returns a user object from a given IP address.
        
        Args:
            ip: A str IP address.
            
        Returns:
            A User associated with the IP.
        """
        return self.all_users[ip]
    
    def online_user(self, ip: str) -> User:
        """Adds User to both online users and all users.
        
        User must already exists in server list.
        Does nothing if user is banned.
        
        Args:
            ip: A str IP address.
            
        Returns:
            The associated User object.
        """
        # do nothing if user is banned
        if ip in self.banned_users:
            return
        if ip in self.all_users:
            user = self.all_users[ip]
            self.online_users[ip] = user
            return user

    def offline_user(self, ip: str) -> None:
        """Moves user to offline.

        Args:
            ip: A str IP address.
            
        Returns:
            None.
        """
        if ip in self.online_users:
            self.online_users.pop(ip)
            
    def is_online(self, ip: str) -> bool:
        """Checks if the IP address is online.
        
        Args:
            ip: A str IP address.
            
        Returns:
            A bool indicating user status.
        """
        return ip in self.online_users
            
    def non_senders(self, ip: str) -> list:
        """Returns a list of online Users that
        does not contain the given ip.
        
        Args:
            ip: A str IP address.
            
        Returns:
            A list of online User objects. An empty list
            is returned if give ip is does not exist.
        """
        result = []
        if ip not in self.online_users:
            return result
        for ip_key, user in self.online_users.items():
            # skip user if ip matches
            if ip_key == ip:
                continue
            result.append(user)
        return result
    
    def contains_user(self, ip: str) -> int:
        """Checks if user exists.

        Args:
            ip: A str IP address.
            
        Returns:
            An int -1, 0, or 1.
                 1 - indicates a user exists and is not banned.
                 0 - indicates a user does not exist.
                -1 - indicates a user is banned.
        """
        # user exists & not banned
        if ip in self.all_users:
            return 1
        # banned user
        elif ip in self.banned_users:
            return -1
        # user doesn't exist
        else:
            return 0

    def kick_user(self, ip: str) -> None:
        """Kicks user from room.

        Args:
            ip: string

        Returns:
            None.
        """
        NotImplemented
        
    def ban_user(self, ip: str) -> None:
        """Bans user from a given IP address.
        
        User is banned by ip address. Anyone else
        with the same ip will also be banned.

        Args:
            ip: A str IP address.
            
        Returns:
            None.
        """
        if ip in self.online_users:
            self.online_users.pop(ip)
        if ip in self.all_users:
            self.banned_users[ip] = self.all_users.pop(ip)
        
    def unban_user(self, ip: str) -> None:
        """Unbans a user from a given IP address.
        
        User is unbanned by ip address. Anyone else
        with the same ip will also be unbanned.
        
        Args:
            ip: A str IP address.
            
        Returns:
            None.
        """
        if ip in self.banned_users:
            self.banned_users.pop(ip)
        
    def read_instance(self, filepath: str='connection_manager.pkl') -> IO:    
        """Reads an instance of the ConnectionManager object from the filepath.
        
        Instance is read using pickle.HIGHEST_PROTOCOL.
        
        Args:
            filepath: An (optional) file path to read the ConnectionManager
                object in. Defaults to 'connection_manager.pkl'
            
        Returns:
            None.
        """
        # get directory path
        dir_path = os.path.split(filepath)[0]
        if not dir_path:
            dir_path = '.'
        # check if file exists
        if filepath in os.listdir(dir_path):
            with open(filepath, 'rb') as f:
                rdata = pickle.load(f)
                # set user information
                self.all_users, self.banned_users = rdata
        else:
            print(f'No such file {filepath}.')
        
    def save_instance(self, filepath: str='connection_manager.pkl') -> IO:
        """Saves an instance of the ConnectionManager object to the filepath.
        
        Instance is written using pickle.HIGHEST_PROTOCOL.
        
        Args:
            filepath: An (optional) file path to store the ConnectionManager
                object in. Defaults to 'connection_manager.pkl'
            
        Returns:
            None.
        """
        wdata = (self.all_users, self.banned_users)
        with open(filepath, 'wb') as f:
            pickle.dump(wdata, f, pickle.HIGHEST_PROTOCOL)
        