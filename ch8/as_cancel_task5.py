# this example shows how task management can bekle
# made using wait() method. This method provides
# a means to await a series of tasks depending
# on a condition. This example assumes that
# if any one of the tasks are ended the blocking 
# wait ends which is determined by the method 
# parameter: (return_when=asyncio.FIRST_COMPLETED).

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
    #while True: # infinite execution
    while (i<10):# ends normally at 10th second        
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
    pending = (task1, task2, task3)
    
    # if while loop in the timer task is set
    # infinite, this loop will also be infinite.
    # in this case we need to determine a retry
    # limit when reached the task is cancelled
    # automatically. 
    while pending:# cont. if pending list is full
        done, pending = await asyncio.wait(
            pending,
            return_when=asyncio.FIRST_COMPLETED
        ) # with the first task completed, the blocking await ends
        # the results from done tasks lists are drawn and displayed
        result = done.pop().result()
        print(f"result: {result}")

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
