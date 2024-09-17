from enum import Enum

class AuthStatus(Enum):
    SUCCESS = 1
    EXPIRED = 2
    UNAUTHORIZED = 3