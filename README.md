# Memealerts Python Client

This project is a library which provides you clients for interaction with memealerts.

# Install

`pip install memealerts`

# Usage

## Using sync client
```python
from memealerts import MemealertsClient

token = "<Your bearer token>"

cli = MemealertsClient(token)

supporters = cli.get_supporters()
first_supporter = supporters.data[0].supporterId
cli.give_bonus(first_supporter, 5)
```

## Using async client

```python
import asyncio
from memealerts import MemealertsAsyncClient

token = "<Your bearer token>"

cli = MemealertsAsyncClient(token)

async def main():
    supporters = await cli.get_supporters()
    first_supporter = supporters.data[0].supporterId
    await cli.give_bonus(first_supporter, 5)

asyncio.run(main())
```

# Badges

[![wakatime](https://wakatime.com/badge/github/Quantum-0/memealerts.svg)](https://wakatime.com/badge/github/Quantum-0/memealerts)
[![Black](https://github.com/Quantum-0/memealerts/actions/workflows/black.yml/badge.svg)](https://github.com/Quantum-0/memealerts/actions/workflows/black.yml)
[![GitHub Org's stars](https://img.shields.io/github/stars/quantum-0/memealerts)](https://github.com/Quantum-0/memealerts/)
![PyPI - License](https://img.shields.io/pypi/l/memealerts)
[![PyPI](https://img.shields.io/pypi/v/memealerts)](https://pypi.org/project/memealerts/)
![PyPI - Status](https://img.shields.io/pypi/status/memealerts)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/memealerts)
![PyPI - Downloads](https://img.shields.io/pypi/dm/memealerts)


# License

[MIT License](./LICENSE)

# TODO

- handle errors from api
- iterator for all supporters
- user/find
- other methods and schemas
- 