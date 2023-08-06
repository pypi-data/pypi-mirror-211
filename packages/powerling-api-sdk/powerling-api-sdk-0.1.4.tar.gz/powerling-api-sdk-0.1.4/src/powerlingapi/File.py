
from . import exceptions

class File():
  """
  Class reprensenting a Powerling API file
  """

  def __init__(self, api_instance, order_id: int, file_data: dict):
    """
    ### Parameters:
    `order_id` : int
      The order id.
    `api_instance` : PowerlingAPI
      The PowerlingAPI instance.
    `file_data` : dict
      The file data.
      {}
    """
    self.orderid = order_id
    self.session = api_instance.session
    self.url = api_instance.url
    self.id = file_data['id']
    self.status = file_data['status']
    if (file_data.get('clientref') != None):
      self.clientref = file_data['clientref']

  def __str__(self) -> str:
    if (self.clientref != None):
      return f'id={self.id}, name={self.status}, clientref={self.clientref}'
    else:
      return f'id={self.id}, name={self.status}'

  def __repr__(self) -> str:
      return f'<powerlingapi.File id={self.id}>'

  def status(self) -> str:
    """
    ### Returns:
    `str`: The file status.
    """
    res = self.session.get(self.url + 'order/' + str(self.orderid) + '/file/' + str(self.id) + '/status')
    return res.json()

  def download(self) -> dict:
    """
    ### Returns:
    `None`: The file is downloaded.

    ### Raises:
    `exceptions.file.StatusIsNotComplete`: The file status is not `complete`.
    """
    if (self.status != 'complete'):
      raise exceptions.file.IsNotComplete
    res = self.session.get(self.url + 'order/' + str(self.orderid) + '/file/' + str(self.id))
    return res.json()

  def add_callback(self, callback_url: str) -> dict:
    """
    ### Parameters:
    `callback_url` : str
      The callback url.
    ### Returns:
    `None`: The callback is added.
    """
    res = self.session.post(self.url + 'order/' + str(self.orderid) + '/file/' + str(self.id) + '/request-callback', data={'url': callback_url})
    return res.json()

  def get_analysis(self):
    """
    ### Returns:
    `dict`: The file analysis.
    """
    res = self.session.get(self.url + 'order/' + str(self.orderid) + '/file/' + str(self.id) + '/analysis')
    return res.json()