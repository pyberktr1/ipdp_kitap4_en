# this example shows the use of queues in asynchronous programs.
# in this example a series of stone grinding units (consumers)
# are fed by a single feeder (producer) is modeled as a simulation.
# the stoneks are connected through a queue.

# async io library
import asyncio
# time library
import time
# random number library 
import random

# total grinded stone counter
tot_stones = 0#kg

# stone feeder coro
async def stone_feeder(feeder):
    global tot_stones 
    for _ in range(36):# feed 36 stones
        stone = random.uniform(0.5, 1.5)#kg
        tot_stones += stone# total production
        # throw stones to the queue
        await feeder.put(stone) 
        # process delay
        await asyncio.sleep(random.uniform(0.1,0.2))
        
    # feeder ok
    print("Producer: feeding completed!")
    
# stone grinding coro
async def stone_grinder(no, feeder):
    while True:# infinite loop
        # get a stone from queue
        stone = await feeder.get()

        # wait for grinding (1kg=1s, 2kg=2s)
        await asyncio.sleep(stone)

        # stone grinding completed
        feeder.task_done()

        print(f"stone grinder#{no}, grinded {stone:2.3f} kg stone")

# main coro
async def main():
    # global variables
    global tot_stones
    
    # feeder queue created
    feeder = asyncio.Queue()#maxsize=1)
    
    # wait for all stones to be grinded
    start = time.perf_counter()# start time

    
    # producer task
    stone_feed = asyncio.create_task(stone_feeder(feeder))
    
    # 4 consumer task (stone grinders)
    stone_grinders = []
    for i in range(4):
        task = asyncio.create_task(stone_grinder(i, feeder))
        stone_grinders.append(task)
     
    # wait for all task to start
    await asyncio.sleep(1)
    
    # wait till the queue dries
    await feeder.join() 
    
    # stop time
    stop = time.perf_counter()

    # we cancel all the stone grinder tasks
    for task in stone_grinders:
        task.cancel()
        
    # we wait to ensure all tasks are cancelled
    await asyncio.gather(*stone_grinders, return_exceptions=True)

    print(f"4 stone grinders in {stop - start:2.3f} seconds,",
          f"\ngrinded {tot_stones:2.3f} kg stones totally ")
          
# main program block
if __name__ == '__main__':
    asyncio.run(main())