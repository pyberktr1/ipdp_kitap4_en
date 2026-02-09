# this example shows asynchronous file operations

# async io library
import asyncio
# time library
import time
# asynchronous file library
# use "python3 -m pip install aiofiles" to install
import aiofiles
# os function for random number generation
import os

# program constants
# packet size 
p_size = 4096 # (bytes)
# packet count per file 
p_count = 1000 
# number of concurrent files
f_count = 5 

# the generator coro for producing random numbers
# in packets
async def agenerator():
    while True:
        # p_size random bytes
        yield os.urandom(p_size)

# asynchronous file coro
async def afiles(file):
    au = agenerator()# asynchronous generator object
    # draw packets from the agenerator and write to the file
    async with aiofiles.open(file, mode="wb") as d:
        i=0# packet counter
        # fetch packets
        async for packet in au:
            # write packets to file
            await d.write(packet)            
            i+=1# increment packet counter
            if i>=p_count:# stop at p_count
                break
    
# main coro
async def main():
    print("writing to files starts...")
    # start time
    start = time.perf_counter()
    # we start the tasks
    g = await asyncio.gather( *(afiles(f".\\files\\file{i}.rnd") 
                                  for i in range(f_count)), 
                              return_exceptions=True )
    # stop time
    stop = time.perf_counter()
    print("all writes to files are completed!")
    print("RESULTS")
    print(g)# None means "no errors"
    print(f"\nexecution time:{stop-start:2.3f} seconds")
    
# main program block
if __name__ == "__main__":
    asyncio.run(main())
    