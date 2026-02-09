# this example shows the operation details of an asynchronous sleep()

# async io library
import asyncio
# time library
import time

# the class used to transfer execution control to event loop
class evloop_yield:
    def __await__(self):
        yield# stop execution and transfer control to evloop

# equivalent asleep() coro
async def asleep(s:float):
    # calculate awake time
    awake = time.time() + s # saniye
    while True:# infinite loop
        # has awake time come?
        if time.time() >= awake:
            return# close
        else:# there is time to awake
            # transfer control to evloop
            await evloop_yield()

# an asynchronous task that makes the evloop busy
async def task():
    p=0
    for i in range(10**9):
        p+=1
    print("task complete!")
    
# main coro
async def main():
    print("all tasks are started!")
    # start time
    start = time.perf_counter()
    # a task is desgined to busy the evloop
    g=asyncio.create_task(task())
    # sleep task started
    #await asyncio.sleep(2)
    await asleep(2)
    
    # stop time
    stop = time.perf_counter()
    print(f"execution time:{stop-start:2.3f}")
    await g
    
# main program block
if __name__ == "__main__":
    asyncio.run(main())
        
