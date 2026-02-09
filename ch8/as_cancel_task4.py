# this example shows cancellation of a task
# after a series of timeouts which is 
# shielded against cancellation 

# async io library
import asyncio
# time library
import time

# a coro definition
async def as_cube(number: int) -> int:
    print("cubing starts!")
    # process delay
    await asyncio.sleep(3)# seconds
    print("cubing completed!")
    return number**3

# another coro definiton 
async def as_square(number: int) -> int:
    print("squaring starts!")
    # islem suresini temsil eden gecikme
    await asyncio.sleep(2)# saniye bekle
    print("squaring completed!")
    return number**2

# timer coro  
async def timer():
    i=0
    # select one of the loops for
    # different closing scenarios
    while True: # infinite execution
    #while (i<10):# ends normally at 10th second        
        await asyncio.sleep(1)
        i+=1
        print(f"seconds: {i}")
    return f"Timer stopped at {i} second..."
    
# main coro
async def main():
    
    # first task 
    task1 = asyncio.create_task(as_cube(2))
    
    # second task 
    task2 = asyncio.create_task(as_square(3))
    
    # timer task
    task3 = asyncio.create_task(timer())
    
    # now we are ready to await
    
    # await for first task 
    cubes   = await task1
    print(f"cubes  : {cubes}")
    
    # await for second task
    squares = await task2
    print(f"squares: {squares}")    
    
    # since all the tasks are completed we can 
    # cancel the timer task here we set a 3 seconds
    # timeout limit.
    # if the number of timeouts are reached to the max.
    # retry value and the task is still alive than we
    # force it to close.
    max_retries = 3    # retry limit
    timo_st     = True # timeout status
    n_retries   = 0    # retry counter
    # if there is a timeout but max_retires limit is not reached
    # than retry once more
    result  = None 
    timo_st = True
    while (timo_st and (n_retries < max_retries)):
        # task3 is awaited
        try:
            result = await asyncio.wait_for(asyncio.shield(task3), 
                                            timeout=3)
            timo_st = False # task has ended without a timeout
        except TimeoutError:# task is timed out
            print("Timer task took longer than expected!")
            n_retries+=1    # increment retry counter
            print(f"Number of retries: {n_retries}")
    # if loop is ended with a time out status than max retries
    # limit has been exceeded. otherwise the task ended normally    
    if timo_st:# is max retries limit exceeded?
        print("Max. retries limit is exceeded.",
              "\nThe task will be forced to close!")
        if not task3.done():
            print('Timer task will be cancelled...')
            task3.cancel()
    else:
        print(f"Timer task has ended normally. Result :{result}")

# main program block
if __name__ == '__main__':
    
    # start time
    print("LET THE CODE EXECUTION BEGIN!")
    start = time.perf_counter()
    
    # call to main coro
    res=asyncio.run(main())
    
    # stop time
    stop = time.perf_counter()
    print("CODE EXECUTION COMPLETED!")
    print(f"execution time: { stop - start : 2.3f}")
