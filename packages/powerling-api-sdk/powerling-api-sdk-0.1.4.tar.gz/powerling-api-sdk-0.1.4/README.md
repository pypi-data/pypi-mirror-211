# Powerling API SDK

## Installation
### From sources
```bash
git clone <url> power-api-sdk
cd power-api-sdk
pip install .
```

### From `test pypi`
```bash
pip install -i https://test.pypi.org/simple/ powerling-api-sdk-package-powerling
```

## Usage

<!-- ### ~~Configuration~~ -->

### Initialization
```py
from powerlingapi import PowerlingApi
from powerlingapi import exceptions

def main():
  api = PowerlingApi()

  try:
    api.authorize("YOUR-ACCESS-TOKEN")

  except exceptions.api.InvalidCredentials as error:
    print(error)
```

### Account

```py
from powerlingapi import PowerlingApi
from powerlingapi import exceptions
from powerlingapi import Form

def main():
  # [initialization...]

  api.account()
```

### Supported languages

```py
from powerlingapi import PowerlingApi
from powerlingapi import exceptions
from powerlingapi import Form

def main():
  # [initialization...]

  api.supported_langs()
```

### Order

#### Create

```py
from powerlingapi import PowerlingApi
from powerlingapi import exceptions
from powerlingapi import Form

def main():
  # [initialization...]

  new_order = Form.Order("New order")

  try:
    order = api.create_order(new_order)

  except exceptions.order.ErrorOnCreation as error_on_creation:
    print(error_on_creation)

  except Exception as error:
    print(error)
```

#### Get

```py
from powerlingapi import PowerlingApi
from powerlingapi import exceptions

def main():
  # [initialization...]

  try:
    order = api.get_order_by_id(123)

  except exceptions.order.NotFound as error_not_found:
    print(error_not_found)

  except Exception as error:
    print(error)
```

#### Submit

```py
from powerlingapi import PowerlingApi

def main():
  # [initialization...]

  # [get an order with id or create new one]
  order.submit()
```

#### Add callback

```py
from powerlingapi import PowerlingApi

def main():
  # [initialization...]

  url = "https://exemple.com/callback"

  # [get an order with id or create new one]
  order.add_callback(url)
```

#### Get analysis

```py
from powerlingapi import PowerlingApi

def main():
  # [initialization...]

  # [get an order with id or create new one]
  order.get_analysis()
```

#### Add binary file

```py
from powerlingapi import PowerlingApi
from powerlingapi import exceptions
from powerlingapi import Form

def main():
  # [initialization...]

  try:
    form_file = Form.FileBinary('fr_FR', 'de_DE', 'file.xlf')

    # [get an order with id or create new one]
    file_id = order.add_bin_file(form_file)

  except exceptions.form.InvalidFormFileBinary as invalid_form:
    print(invalid_form)

  except exceptions.file.ErrorOnUpload as error_on_upload:
    print(error_on_upload)

  except Exception as error:
    print(error)
```

#### Add url file

```py
from powerlingapi import PowerlingApi
from powerlingapi import exceptions
from powerlingapi import Form

def main():
  # [initialization...]

  try:
    form_file = Form.FileUrl('fr_FR', 'de_DE', 'https://exemple.com/file.xlf')

    # [get an order with id or create new one]
    file_id = order.add_url_file(form_file)

  except exceptions.form.InvalidFormFileUrl as invalid_form:
    print(invalid_form)

  except exceptions.file.ErrorOnUpload as error_on_upload:
    print(error_on_upload)

  except Exception as error:
    print(error)
```

### File

#### Get

```py
from powerlingapi import PowerlingApi

def main():
  # [initialization...]

  # [get an order with id or create new one]
  files = order.get_files() # Get all files attached to the order

  the_file = order.get_file_by_id(123) # Get specific file from the order

  completed_files = order.get_files_by_status("completed") # Get all files with specific status

```

#### Status

```py
from powerlingapi import PowerlingApi

def main():
  # [initialization...]

  # [get a file]
  file.status()
```

#### Download

```py
from powerlingapi import PowerlingApi

def main():
  # [initialization...]

  # [get a file]
  file.download()
```

#### Add callback

```py
from powerlingapi import PowerlingApi

def main():
  # [initialization...]

  url = "https://exemple.com/callback"

  # [get a file]
  file.add_callback(url)
```

#### Get analysis

```py
from powerlingapi import PowerlingApi

def main():
  # [initialization...]

  # [get a file]
  file.get_analysis()
```