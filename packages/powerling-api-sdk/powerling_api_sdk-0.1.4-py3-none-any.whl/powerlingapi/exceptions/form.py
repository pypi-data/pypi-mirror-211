class FormException(Exception):
  """
  Base class for exceptions in Form.
  """
  pass

class InvalidFile(FormException):
  """
    Exception raised when a file is not valid.
  """
  def __init__(self, message="Invalid file"):
    super().__init__(message)

class UnknownType(FormException):
  """
    Exception raised when a type is not valid.
  """
  def __init__(self, message="Unknown type"):
    super().__init__(message)

class InvalidFormFileBinary(InvalidFile):
  """
    Exception raised when a file is not valid.
  """
  def __init__(self, message="Invalid binary Form"):
    super().__init__(message)

class InvalidFormFileUrl(InvalidFile):
  """
    Exception raised when a file is not valid.
  """
  def __init__(self, message="Invalid url Form"):
    super().__init__(message)