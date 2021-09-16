import json
from os import path
from helpers.typing import JSONType


def load_data(name) -> JSONType:
  """
  Takes the name of the data you wish to retrieve (without a file extension), loads it, and returns it.

  ```python
  zip_codes = load_data('zip_codes')
  texas_zip_codes = zip_codes['TX']
  ```
  """
  with open(path.join(path.dirname(__file__), f'{name}.json')) as data_file:
    return json.load(data_file)
