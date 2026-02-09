# this example shows the results of using synchronous for
# loops in asynchronous applications.

# async io library
import asyncio
# time library
import time

# synchronous generator
def generator():
    i=0# initial value
    while i<10:# count 9
        # process delay
        time.sleep(0.5)        
        yield i
        i+=1# increment value

# coro that uses a synchronous for loop
async def for_loop(fid):
    # loop ends when no values are generated more
    for i in generator():
        print(f"{fid}::{i}")
        
# main coro
async def main():
    # start time
    start = time.perf_counter()
    # tasks are started
    g = await asyncio.gather(*(for_dongu(i) for i in range(2)))
    # stop time
    stop = time.perf_counter()
    print(f"execution time:{stop-start:2.3f}")
    
# main program block
if __name__ == "__main__":
    asyncio.run(main())
    