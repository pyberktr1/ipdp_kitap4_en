# this example shows the use of anext() method for
# asynchronous data yielding

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

# drawing data from an asynchronous generator
# using anext() method
async def anext_loop(fid):
    # generator object
    y = generator() 
    # inifinite loop is broken when "StopAsyncIteration"
    # excpetion is raised in the case of generator
    # has no values to yield
    while True:
        try:
            # draw values from generator
            i = await anext(y)
            print(f"{fid}::{i}")
        except StopAsyncIteration:# no values to yield
            break
        
# main coro
async def main():
    # start time
    start = time.perf_counter()
    # start tasks
    g = await asyncio.gather(*(anext_loop(i) for i in range(2)))
    # stop time
    stop = time.perf_counter()
    print(f"execution time:{stop-start:2.3f}")
    
# main program block
if __name__ == "__main__":
    asyncio.run(main())
    