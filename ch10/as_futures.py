# this examples shows the operation of futures

# async io library
import asyncio
# time library
import time

# the task that sets the future
async def task(future):
    # 3 seconds delay
    await asyncio.sleep(3)
    future.set_result("future NOW") 

# main coro
async def main():
    # we create a future to be awaited
    future = asyncio.Future()
    
    # we create a task that sets the future
    # after a brief delay
    g=asyncio.create_task(task(future))

    print("future is awaited!")
    # start time
    start = time.perf_counter()
    # future is awaited 
    # the wait ends with the setting of
    # the future
    result = await future
    # stop time
    stop = time.perf_counter()
    print(f"future result : {result}")
    print(f"execution time:{stop-start:2.3f}")
    # we are waiting for the task end
    await g
    
# main program block
if __name__ == "__main__":
    asyncio.run(main())
        
