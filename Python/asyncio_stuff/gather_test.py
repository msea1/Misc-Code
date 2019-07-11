import asyncio


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")


async def downlink():
    print("Task starting downlink")
    await asyncio.gather(
            factorial("A", 2),
            factorial("B", 3),
            factorial("C", 4),
        )
    print(f"Downlink complete")


async def uplink():
    print("Task starting uplink")
    await asyncio.gather(
            factorial("E", 2),
            factorial("F", 3),
        )
    print(f"Uplink complete")


async def quick():
    print('!!!!!!!!!!!!!!!!!!!!!! Hello from quick')


async def main_before():
    quick_task = asyncio.ensure_future(quick())
    await downlink()
    await uplink()
    await quick_task


async def main():
    # await asyncio.gather(downlink(), uplink())
    await downlink()
    await uplink()
    quick_task = asyncio.get_event_loop().create_task(quick())
    # quick_task = asyncio.ensure_future(quick())
    await quick_task


asyncio.get_event_loop().run_until_complete(main())
