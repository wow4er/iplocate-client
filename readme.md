# iplocate-client

Python client for [iplocate.net](https://iplocate.net) — IP geolocation API.

## Installation

```
pip install iplocate-client
```

## Quick start

```python
from iplocate_client import IPLocate

client = IPLocate()

# Your current IP
client.lookup()

# Specific IP
client.lookup("8.8.8.8")

# Only specific fields
client.lookup("8.8.8.8", fields=["country", "city", "asn"])
```

## Bulk lookup

Free tier: 50 req/min. With API key (free, requires account on [iplocate.net](https://iplocate.net)): 250 req/min.
```python
client = IPLocate(api_key="your_api_key")
results = client.bulk(["8.8.8.8", "1.1.1.1"])
```

Max 20 IPs per request.

## Async

```python
from iplocate_client import AsyncIPLocate

client = AsyncIPLocate()
data = await client.lookup("8.8.8.8")
results = await client.bulk(["8.8.8.8", "1.1.1.1"])
```

## Available fields

`city` `continent` `country` `country_iso` `latitude` `longitude` `timezone` `postal` `asn` `asn_number`

Response always includes `ip` and `ip_ver`.

## Error handling

```python
from iplocate_client import RateLimitError, InvalidIPError

try:
    client.lookup("bad_ip")
except InvalidIPError as e:
    print(e)
except RateLimitError:
    print("slow down")
```

## License

MIT