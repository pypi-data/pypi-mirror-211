class OrderException(Exception):
  """
    Base class for exceptions in Order.
  """
  pass

class NotFound(OrderException):
  """
  Exception raised when an order is not found.
  """
  def __init__(self, message="Order not found"):
    super().__init__(message)

class ErrorOnCreation(OrderException):
  """
    Exception raised when order creation failed.
  """
  def __init__(self, message="Error on order creation"):
    super().__init__(message)