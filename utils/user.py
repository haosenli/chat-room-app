"""This file contains the User class.
"""


class User:
    """User provides a simple data structure to store user information.
    """
    def __init__(self, username: str, ip: str) -> None:
        """Constructs a User object from a username and ip.
        
        Args:
            username: A str username of a user.
            ip: A str ip address of a user.
            
        Returns:
            None.
        """
        self.username = username
        self.ip = ip
        # self.conn = conn
        # self.addr = addr
        
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