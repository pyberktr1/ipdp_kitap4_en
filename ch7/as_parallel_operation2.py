# this example shows the parallel (collective or
# asynchronous) operation of coros 
# the program ends prematurely due not waiting tasks.

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
    # asynchronous execution of coros
    # we need to packet coros as tasks and send
    # these tasks to event loop for execution
    # in a round robin fashion.
    # parallel operation mandates that two coros
    # operate on unrelated inputs.
    # first coro task (does not block)
    task1 = asyncio.create_task(as_cube(2))
    
    # second coro task (does not block also)
    task2 = asyncio.create_task(as_square(3))
    
    # now we are ready to await tasks (not coros)
    # the waits in the tasks will be managed by the event loop
    # event loop uses blank parts (awaits) in the code of the
    # coros to execute code that belong to other coros.
    # By this way it is possible to execute coros concurrently.
    # this makes it mandatory to use design principle in the
    # coros that promote collective operation (not race or competition).
    
    # first task is called without awaiting (not blocks)
    cubes   = task1
    print(f"cubes: {cubes}")
    
    # econd task (is called without awaiting (not blocks also)
    squares = task2
    print(f"squares: {squares}")
        
    # since we did not await the tasks, the main coro completes
    # immediately and we had no time to collect the results
    # from corresponding tasks. This condition is also warned
    # by a message that says the tasks did not awaited.

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
