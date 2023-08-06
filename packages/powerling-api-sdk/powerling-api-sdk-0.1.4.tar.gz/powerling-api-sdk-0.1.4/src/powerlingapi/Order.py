
from typing import List, Union

from .File import File
from . import Form
from . import exceptions

class Order():
  """
  Class reprensenting a Powerling API order
  """

  def __init__(self, api, id: int, order: dict):
    """
    ### Parameters:
    `api` : PowerlingAPI
      The Powerling API object.
    `id` : int
      The order id.
    `order` : dict
      The order informations.
    """
    self.id = id
    self.session = api.session
    self.url = api.url

    self.status = order['data']['status']
    self.files = []
    for file in order['data']['files']:
      self.files.append(File(api, id, file))

  def __str__(self) -> str:
    return f'id: {self.id}, status=\'{self.status}\''

  def __repr__(self) -> str:
      return f'<powerlingapi.Order id={self.id}>'

  def get_files(self) -> list:
    """
    ### Returns:
    `list`: The list of files.
    """
    return self.files

  def get_file_by_id(self, id: int) -> Union[File, None]:
    """
    ### Parameters:
    `id` : int
      The file id.
    """
    for file in self.files:
      if (file.id == id):
        return file
    return None

  def get_files_by_status(self, status: str) -> List[File]:
    """
    ### Parameters:
    `status` : str
      The file status.
    """
    files = []
    for file in self.files:
      if (file.status == status):
        files.append(file)
    return files

  def add_bin_file(self, form: Form.FileBinary) -> int:
    """
    ### Parameters:
    `form` : Form.FileBinary
      The form data.

    ### Returns:
    `int`: The file id.

    ### Raises:
    `exceptions.file.ErrorOnUpload`: If the file upload failed.
    """
    res = self.session.post(self.url + 'order/' + str(self.id) + '/upload-file', files=form.get())
    data = res.json()
    if (data.get('success') == False):
      raise exceptions.file.ErrorOnUpload(data['error'])
    return data['fileid']

  def add_url_file(self, form: Form.FileUrl) -> int:
    """
    ### Parameters:
    `form` : Form.FileUrl
      The form data.

    ### Returns:
    `int`: The file id.

    ### Raises:
    `exceptions.file.ErrorOnUpload`: If the file upload failed.
    """
    res = self.session.post(self.url + 'order/' + str(self.id) + '/add-file', data=form.get())
    data = res.json()
    if (data.get('success') == False):
      raise exceptions.file.ErrorOnUpload(data['error'])
    return data['fileid']

  def submit(self):
    """
    ### Returns:
    `bool`: True if the order is submitted.
    """
    res = self.session.post(self.url + 'order/' + str(self.id) + '/submit')
    return res.json()

  def add_callback(self, callback_url: str) -> None:
    """
    ### Parameters:
    `callback_url` : str
      The callback url.

    ### Returns:
    `None`
    """
    res = self.session.post(self.url + 'order/' + str(self.id) + '/request-callback', data={'url': callback_url})

  def get_analysis(self) -> dict:
    """
    ### Returns:
    `dict`: The analysis informations.
    """
    res = self.session.get(self.url + 'order/' + str(self.id) + '/analysis')
    return res.json()