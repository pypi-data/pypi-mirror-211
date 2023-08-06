# engine4-python

⚙️ Python library for the ENGINE4 API.

## Installation

Use [pip](https://pypi.org/project/pip/) to install the package:

```
pip3 install engine4
```

## Usage

First of all, you import `ENGINE4` so that you can create an instance of the class.
You need to pass the `base_url` of the API server:

```py
from engine4 import ENGINE4

engine4 = ENGINE4('https://test.engine4.io/')
```

Now you can authenticate yourself with `username`, `password` and `client_id`:

```py
def authenticate() -> str:
  username = 'my_username'
  password = 'my_password'
  client_id = 'my_client_id'
  result = engine4.authenticate(username, password, client_id)
  return result.access_token
```

The access token is required for the following calls.

Here you can find examples:

```py
from engine4 import FetchFilterOptions

access_token = authenticate()

def fetch() -> list:
  entity_id = '12e2eb88-814a-0a98-40e2-b006586dfd59'
  skip = 0
  take = 2
  with_long_values = False
  is_active = True
  filter = FetchFilterOptions('CreatedDate', '>', '2018-01-01T00:00:00.000Z')
  result = engine4.fetch(access_token, entity_id, skip, take, False, is_active, filter)
  return fetch_result['items']
```

## Changelog

See [CHANGELOG.md](https://github.com/robingenz/engine4-python/blob/main/CHANGELOG.md).

## License

See [LICENSE](https://github.com/robingenz/engine4-python/blob/main/LICENSE).
