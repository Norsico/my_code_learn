import asyncio, time

async def some_work():
    print("Work")
    await asyncio.sleep(1)
    # time.sleep(1)
    print("Work Done")

async def play():
    print("Play")
    await asyncio.sleep(2)
    print("Play End")

async def main():
    # print("Start")
    # await asyncio.gather(play(), some_work())
    task = asyncio.create_task(some_work())
    print("Done1")
    # time.sleep(1)
    await task
    await asyncio.create_task(play())
    print("Done2")

asyncio.run(main())
