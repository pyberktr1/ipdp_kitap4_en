# this example shows task shielding
# against cancellation

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
    while True:
        await asyncio.sleep(1)
        i+=1
        print(f"seconds: {i}")

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
    try:
        await asyncio.wait_for(
        asyncio.shield(task3), timeout=3)
    except asyncio.TimeoutError:
        print("Timer task took longer than expected!")
    
    # we wait for an additional 5 seconds
    # after which we end the main coro which
    # ensures automatic cancellation of all waiting tasks
    await asyncio.sleep(5)
    print("Program and all the ",
          "waiting tasks will be closed...")

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
