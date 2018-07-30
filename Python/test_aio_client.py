import asyncio
import aiohttp


client_connector = aiohttp.TCPConnector(verify_ssl=False, loop=asyncio.get_event_loop())
client_session = aiohttp.ClientSession(connector=client_connector)


async def foo():
    async with client_session.get('http://localhost:8080/hello') as resp:
        print(resp)
        # resp.raise_for_status()

    print('\nNow the exception \n\n')
    async with client_session.get('http://localhost:8080/exc') as resp:
        print(resp)
        # resp.raise_for_status()

    print('\nNow the AIO exception \n\n')
    async with client_session.get('http://localhost:8080/exc_new') as resp:
        print(resp)
        # resp.raise_for_status()

asyncio.get_event_loop().run_until_complete(foo())
