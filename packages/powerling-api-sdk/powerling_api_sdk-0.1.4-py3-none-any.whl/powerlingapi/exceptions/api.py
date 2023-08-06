class PowerlingApiException(Exception):
    """
    Base class for exceptions in this module.
    """
    pass

class InvalidCredentials(PowerlingApiException):
    """
    Exception raised when the credentials are not valid.
    """
    def __init__(self, message="Invalid credentials"):
        super().__init__(message)