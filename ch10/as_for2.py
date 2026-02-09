# this example shows the results of using asynchronous for
# loops in asynchronous applications.

# async io library
import asyncio
# time library
import time

# asynchronous generator
async def generator():
    i=0# initial value
    while i<10:# count 9
        # process delay
        await asyncio.sleep(0.5)        
        yield i
        i+=1# increment value

# coro using asynchronous for loop
async def afor_dongu(fid):
    # loop ends when no values are generated more
    async for i in generator():
        print(f"{fid}::{i}")
        
# main coro
async def main():
    # start time
    start = time.perf_counter()
    # tasks are started
    g = await asyncio.gather(*(afor_dongu(i) for i in range(2)))
    # stop time 
    stop = time.perf_counter()
    print(f"execution time:{stop-start:2.3f}")
    
# main program bolumu
if __name__ == "__main__":
    asyncio.run(main())
    