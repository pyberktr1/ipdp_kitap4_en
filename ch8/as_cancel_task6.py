# this example shows cancellation of a task group
# using a special cancel task

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
    res = number**3
    print(f"cube   : {res}")

# another coro definiton 
async def as_square(number: int) -> int:
    print("squaring starts!")
    # islem suresini temsil eden gecikme
    await asyncio.sleep(2)# saniye bekle
    print("squaring completed!")
    res = number**2
    print(f"square : {res}")

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

# exception class definition that will be used in the cancellation task
class CancelTaskGroup(Exception):
    """task group cancellation exception"""

# the task for forcing the task group to terminate
async def cancel_task_group():
    # with a call to this task, an exception is raised
    raise CancelTaskGroup()

# main coro
async def main():
    
    # we join all tasks under a task group
    try:
        async with asyncio.TaskGroup() as tg:
            # normal tasks are thrown to the task group
            tg.create_task(as_cube(2))
            tg.create_task(as_square(3))
            tg.create_task(timer())
            # we set a reasonable time limit for execution of tasks
            await asyncio.sleep(12)# seconds
            # we throw the cancellation task to the task group 
            # which in turn forces the task group to terminate
            tg.create_task(cancel_task_group())
    # the cancellation exception raised will be handled here
    except* CancelTaskGroup:# there is an exception
        print("All tasks are cancelled!")

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
