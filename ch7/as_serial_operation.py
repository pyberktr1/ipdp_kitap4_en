# this example shows serial (synchronous)
# operation of coros

# async io library
import asyncio
# time library
import time

# a coro definition  
async def as_cube(number: int) -> int:
    print("cubing starts!")
    # operation delay
    # to operate coros as asynchronous functions
    # we need to use coros as sub-routines that 
    # are written using asynchronous methods.
    # we used an asynchronous equivalent of
    # a synchronous sleep() method drawn from
    # time library for this reason. The sleep()
    # method used is drawn from asyncio library
    # for this purpose. 
    # asynchronous operation of coros also
    # need to use the "await" keyword in front
    # of them which proivdes an asynchronous
    # wait for the coro function.
    # await keyword can only be used under a coro,
    # and for only coros.
    # the wait function provided by await has
    # an asynchronous nature which ensures that
    # other coros have a chance to execute
    # their code in the CPU.
    await asyncio.sleep(3)# seconds async delay
    print("cubing completed!")
    return number**3

# another coro definition   
async def as_square(number: int) -> int:
    print("squaring starts!")
    # process delay need for the calculation of the result
    await asyncio.sleep(2)# seconds delay
    print("squaring completed!")
    return number**2

# asynchronous body
# asyncio.run() is used only once
# so we need to define a main coro
# to execute coros asynchronously
async def main():
    # synchronous (serial) execution of coros
    # first coro wait that blocks
    cube = await as_cube(2)
    print()
    print(f"cube: {cube}")
    
    # second coro wait that blocks
    # first coro reault is mandatory
    square = await as_square(cube)
    print()
    print(f"square: {square}")
    

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
