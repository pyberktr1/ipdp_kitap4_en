# this example shows the use of gather() method for
# waiting tasks

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

# main coro
async def main():
    
    # first coro task (does not block)
    task1 = asyncio.create_task(as_cube(2))
    
    # second coro task (does not block also)
    task2 = asyncio.create_task(as_square(3))
    
    # now we are ready to wait for the tasks    
    # using asyncio.gather() we join waits 
    square, cube = await asyncio.gather(task2, task1)
    print(f"square : {square}")
    print(f"cube   : {cube}")
    
# main program block
if __name__ == '__main__':
    
    # start time
    print("LET THE CODE EXECUTION START!")
    start = time.perf_counter()
    
    # call to main coro
    # all the coros operate collectively
    res = asyncio.run(main())
    
    # stop time
    stop = time.perf_counter()
    # since all coros are operated concurrently
    # the results are obtained in a shorter duration
    print("CODE EXECUTION COMPLETED!")
    print(f"execution time: { stop - start : 2.3f}")
