
import json
from . import exceptions

class _FormFile():

  def __init__(self, type: str, source: str, target: str, file_path: str, reference: str = None):
    self.type = type
    self.source = source
    self.target = target
    self.reference = reference
    self.path = file_path
    self.__generate_from_type()

  def __str__(self) -> str:
    return f'{self.type} {self.source} -> {self.target}'

  def __repr__(self) -> str:
    return f'<powerlingapi.FormFile {self.type} {self.source} -> {self.target}>'

  def __generate_from_type(self):
    if (self.type == 'binary'):
      return self.__generate_from_binary()
    elif (self.type == 'url'):
      return self.__generate_from_url()
    else:
      raise exceptions.form.UnknownType

  def __generate_from_binary(self):
    if (self.__is_valid()):
      self.data = {
        'sourcelang': (None, self.source),
        'targetlang': (None, self.target),
        'clientref': (None, (self.reference) if self.reference else None),
        'file': (self.path, open(self.path, 'rb'))
      }
    else:
      raise exceptions.form.InvalidFormFileBinary

  def __generate_from_url(self):
    if (self.__is_valid()):
      self.data = {
        'sourcelang': self.source,
        'targetlang': self.target,
        'clientref': self.reference,
        'fileurl': self.path
      }
    else:
      raise exceptions.form.InvalidFormFileUrl

  def __is_valid(self):
    return (self.source != None and
            self.target != None and
            self.path != None)


class FileBinary(_FormFile):

  def __init__(self, source: str, target: str, file_path: str, reference: str = None):
    """
    ### Parameters:
    `source` : str
      The source language. (e.g. 'en_US')
    `target` : str
      The target language. (e.g. 'fr_FR')
    `file_path` : str
      The path to the file.
    `reference` : str
      The reference.

    ### Raise:
    `exceptions.form.InvalidFormFileBinary`: If the form is invalid.

    ### Returns:
    `Form.FileBinary`: The form file.

    """
    super().__init__('binary', source, target, file_path, reference)

  def get(self):
    """
    ### Returns:
    `dict`: The form data.
    """
    return self.data

class FileUrl(_FormFile):

  def __init__(self, source: str, target: str, file_path: str, reference: str = None):
    """
    ### Parameters:
    `source` : str
      The source language. (e.g. 'en_US')
    `target` : str
      The target language. (e.g. 'fr_FR')
    `file_path` : str
      The file path.
    `reference` : str
      The file clientref.

    ### Raises:
    `exceptions.form.InvalidFormFileUrl`: If the form is invalid.

    ### Returns:
    `Form.FileUrl`: The form file.
    """
    super().__init__('url', source, target, file_path, reference)

  def get(self):
    """
    ### Returns:
    `dict`: The form data.
    """
    return self.data


class _FormOrder():

  def __init__(self, name: str, duedate: str = None, metadata: str = None, reference: str = None):
    self.name = name
    self.duedate = duedate
    self.metadata = metadata
    self.reference = reference

  def __str__(self) -> str:
    return f'{self.name}'

  def __repr__(self) -> str:
    return f'<powerlingapi.FormOrder {self.name}>'

  def get(self):
    """
    ### Returns:
    `dict`: The form data.
    """
    return {
      "name": self.name,
      "duedate": self.duedate,
      "metadata": self.metadata,
      "reference": self.reference
    }

class Order(_FormOrder):

  def __init__(self, name: str, duedate: str = None, metadata: str = None, reference: str = None):
    """
    ### Parameters:
    `name` : str
      The order name.
    `duedate` : str (optional)
      The order duedate.
    `metadata` : str (optional)
      The order metadata.
    `reference` : str (optional)
      The order clientref.
    """
    super().__init__(name, duedate, metadata, reference)