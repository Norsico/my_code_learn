

import asyncio

async def task(name, n):
    print(f'{name} 开始')
    await asyncio.sleep(n)
    print(f'{name} 结束')
    return name

async def main():
    t1 = asyncio.create_task(task('A', 2))
    print('1')
    # await asyncio.sleep(0.5)
    t2 = asyncio.create_task(task('B', 1))
    print('2')
    # await asyncio.sleep(0.5)
    t3 = asyncio.create_task(task('C', 0.1))
    print('3')
    # await asyncio.sleep(0.5)
    await t3
    print('4')
    await t2
    print('5')
    await t1
    print('6')
    print('done')

asyncio.run(main())