import asyncio
import aiohttp


client_connector = aiohttp.TCPConnector(verify_ssl=False, loop=asyncio.get_event_loop())
client_session = aiohttp.ClientSession(connector=client_connector)


async def foo():
    async with client_session.get('http://localhost:8080/') as resp:
        print(resp)
        print(await resp.text)

    print('\nNow the health \n\n')
    async with client_session.get('http://localhost:8080/health') as resp:
        print(resp)

asyncio.get_event_loop().run_until_complete(foo())
