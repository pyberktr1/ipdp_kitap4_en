# this example shows the use of gather() method for
# waiting tasks. Tasks are automatically created from coros.

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
        
    # we are ready to wait for the tasks    
    # using asyncio.gather() we join waits 
    # tasks are created directly from the coros
    # by gather() method. They are executed automatically
    # in the event loop.
    square, cube = await asyncio.gather(as_square(3), as_cube(2))
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
