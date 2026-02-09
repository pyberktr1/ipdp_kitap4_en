# synchronization in asynchronous tasks using events

# async io library
import asyncio
# time library
import time

# play/pause coro
async def play_coro(kid, play):
    print(f"{kid} starts!")
    # repeats three times
    for i in range(3):
        # pause coro execution
        play.clear()
        # wait till active signal
        await play.wait()
        # we have permission to cont.
        print(f"{kid}::operates {i} times")
        # process delay
        await asyncio.sleep(0.5)  
    print(f"{kid} completed its task!")
        
# main coro
async def main():
    # play/pause events
    play1 = asyncio.Event()
    play2 = asyncio.Event()
    
    # start time
    start = time.perf_counter()
    
    # tasks created
    g1=asyncio.create_task(play_coro("coro1", play1))
    g2=asyncio.create_task(play_coro("coro2", play2))
    # control execution of tasks
    for _ in range(3):# play/pause with 1 second interval
        await asyncio.sleep(1)
        play1.set()
        await asyncio.sleep(1)
        play2.set()
    # wait tasks
    await g1
    await g2
    # stop time
    stop = time.perf_counter()
    print(f"execution time:{stop-start:2.3f}")
    
# main program block
if __name__ == "__main__":
    asyncio.run(main())
    