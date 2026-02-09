# this example shows how an asynchronous for loop
# can be used to draw sample data from an asynchronous
# generator coro

# async io library
import asyncio
# time library
import time
# random number library
import random

# an asynchronous generator coro definition   
async def generator():
    sample_no = 0 # sample counter
    while True:   # generate in an infinite loop
        # sample generation delay
        sample_no+=1# next sample
        await asyncio.sleep(0.5) # sample time
        # sample is created
        sample = [sample_no, random.uniform(0, 10)]
        yield sample # send the sample when requested
        
# timer coro  
async def timer():
    i=0
    while True:
        await asyncio.sleep(1)
        i+=1
        print(f"seconds: {i}")

# main coro
async def main():
    asyncio.create_task(timer())# timer task
    # generated samples are drawn by a for loop
    async for sample in generator():
        print(f"sample#{sample[0]} = {sample[1]:2.3f}")
        # end the loop by the 11th sample
        if sample[0]>10:
            print("sampling is stopped!")
            break
     
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
