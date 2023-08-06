import requests

from powerlingapi.Order import Order
from . import Form
from . import exceptions

class PowerlingAPI():
  """
  Class reprensenting a Powerling API interface
  """
  # TODO: Add configparser for url and token
  def __init__(self, sandbox: bool = False):
    """
    ### Parameters:
    `sandbox` : bool, optional
      `True` if the API is in sandbox mode, `False` otherwise.
      The default is False.
    """
    self.sandbox = sandbox
    if (self.sandbox == True):
      self.url = 'https://api-sbx.powerling-tp.com/v1/'
    else:
      self.url = 'https://api.powerling-tp.com/v1/'
    self.session = requests.Session()

  def authorize(self, bearer: str) -> None:
    """
    ### Parameters:
    `bearer` : str
      The bearer token to use for the API.

    ### Notes:
        This method just set the bearer token in the session.
    """
    self.session.headers.update({'Authorization': 'Bearer ' + bearer})
    try:
      self.account()
    except Exception:
      self.session.headers.clear()
      raise exceptions.api.InvalidCredentials

  def account(self) -> dict:
    """
    ### Returns:
    `dict`: json response from the API
      The account informations.
    """
    res = self.session.get(self.url + 'account')
    if (res.status_code != 200):
      raise exceptions.api.InvalidCredentials
    return res.json()

  def supported_langs(self) -> dict:
    """
    ### Returns:
    `dict`: json response from the API
      The supported languages.
    """
    res = self.session.get(self.url + 'supported-langs')
    return res.json()

  def get_order_by_id(self, id: int) -> Order:
    """
    ### Parameters:
    `id` : int
      The order id.

    ### Returns:
    `Order`: The order.

    ### Raises:
      `exceptions.order.NotFound`: If the order can't be found.
    """
    res = self.session.get(self.url + 'order/' + str(id))
    data = res.json()
    if (data.get('success') == None):
      raise exceptions.order.NotFound
    order = Order(self, id, res.json())
    return order

  def create_order(self, order: Form.Order) -> Order:
    """
    ### Parameters:
    `order` : Form.Order
      The order form.

    ### Returns:
    `Order`: The created order.

    ### Raises:
    `exceptions.order.ErrorOnCreation`: If the order can't be created.
    """
    res = self.session.post(self.url + 'order/create', data=order.get())
    data = res.json()
    if (data.get('success') == False):
      raise exceptions.order.ErrorOnCreation(data['error'])
    id = data.get('orderid', None)

    order = self.get_order_by_id(id)
    return order
