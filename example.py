import asyncio
from iplocate_client import IPLocate, AsyncIPLocate, RateLimitError, InvalidIPError

# Sync
client = IPLocate()

# Your own IP
print(client.lookup())

# Specific IP, all fields
print(client.lookup("8.8.8.8"))

# Only specific fields
print(client.lookup("8.8.8.8", fields=["country", "city", "asn"]))

# Bulk lookup (api_key gives higher rate limits)
client_with_key = IPLocate(api_key="k_223d36cc24c7785c71ae424efe9af503")
results = client_with_key.bulk(["8.8.8.8", "1.1.1.1"], fields=["country", "city"])
for r in results:
    print(r)


# Error handling
try:
    client.lookup("i_am_not_an_ip")
except InvalidIPError as e:
    print(f"Invalid IP: {e}")
except RateLimitError:
    print("Slow down")


#  Async
async def main():
    client = AsyncIPLocate()

    data = await client.lookup("8.8.8.8")
    print(data)

    results = await client.bulk(["8.8.8.8", "1.1.1.1"])
    print(results)

asyncio.run(main())