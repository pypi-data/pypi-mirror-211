class FileException(Exception):
  """
    Base class for exceptions in File.
  """
  pass

class IsNotComplete(FileException):
  """
    Exception raised when a file status is not `complete`.
  """
  def __init__(self, message="File status is not complete"):
    super().__init__(message)

class ErrorOnUpload(FileException):
  """
    Exception raised when an error occurs during the upload of a file.
  """
  def __init__(self, message="Error on upload"):
    super().__init__(message)