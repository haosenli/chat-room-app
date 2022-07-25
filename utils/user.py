"""This file contains the User class.
"""
from socket import socket


class User:
    """User provides a simple data structure to store user information.
    """
    def __init__(self, username: str, ip: str, connection: socket) -> None:
        """Constructs a User object from a username and ip.
        
        Args:
            username: A str username of a user.
            ip: A str ip address of a user.
            conn: A socket connection of a user.
            
        Returns:
            None.
        """
        self.username = username
        self.socket = connection
        self.ip = ip
        
    def __str__(self):
        """Returns a str representing the user.
        
        Args:
            None.
        
        Returns:
            A str representing the user.
        """
        return '{' + f'{self.username}: {self.ip}' + '}'
        
    def set_username(self, username: str) -> None:
        """Changes the username of the user.
        
        Args:
            username: A str username of a user.

        Returns:
            None.
        """
        self.username = username
    
    def get_username(self) -> str:
        """Returns the username of the user.

        Args:
            None.

        Returns:
            A str representing the username of a user.
        """
        return self.username

    def set_ip(self, ip: str) -> None:
        """Changes the ip address of a user.
        
        Args:
            ip: A str ip address of a user.
        
        Returns:
            None.
        """
        self.ip = ip
    
    def get_ip(self) -> str:
        """Returns the active user ip address.
        
        Args:
            None.
            
        Returns:
            A str representing the ip address of a user.
        """
        return self.ip
    
    def set_socket(self, connection: socket) -> None:
        """Sets the socket connection of the user.
        
        Args:
            conn: A socket connection.
            
        Returns:
            None.
        """
        self.socket = connection
        
    def get_socket(self):
        """Gets the socket connection of the user.
        
        Args:
            None.
            
        Returns:
            A socket connection.
        """
        return self.socket