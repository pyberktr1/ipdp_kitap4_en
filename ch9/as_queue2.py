# this example shows a practical sample playintask throutaskh a
# soundcard. The asynchronous application uses a queue to
# buffer samples from disk and provide to the soundcard.
# the disk provides samples in a burst fashion with a
# maximum data rate of 400kb/s. 
# on the other hand soundcard consumes the samples
# with a fixed rate of 40kb/s. The averataske data rate
# that the disk can provide is assumed more than the 
# 40kb/s data rate of the soundcard.

# async io library
import asyncio
# time library
import time

# harddisk model
async def disk(acces_time):
    # access delay
    await asyncio.sleep(acces_time)

# harddisk data acqusition coro
async def xmit(buffer, acces_time):
    packet = [33]*4000#4kb packet
    while True:# infinite loop
        # wait disk to repond
        await disk(acces_time)
        # wait until buffer empty
        while buffer.full():
            # retry until buffer empty
            # retry delay at least 1 packet time
            await asyncio.sleep(0.1)
        
        # buffer empty, throw 4kb packet         
        await buffer.put(packet)

# soundcard model
async def snd_card(packet, snd_card_refresh):
    # consume the packet here
    await asyncio.sleep(snd_card_refresh)
 
# soundcard data transfer coro
async def recv(buffer, sample_counter, snd_card_refresh):
    dummy_packet = [0]*4000# will be put instead of a dropped packet
    while True:# infinite loop
        # ensure that buffer is full
        while buffer.empty():
            # drop one packet
            sample_counter["dropped_packet_count"] +=1
            # increment total packet counter also
            sample_counter["total_packet_count"] +=1
            # send the dummy packet to soundcard
            await snd_card(dummy_packet, snd_card_refresh)
        
        # buffer full, get a packet from buffer
        sample_counter["total_packet_count"] +=1
        packet = await buffer.get()
        # send the packet to the soundcard
        await snd_card(packet, snd_card_refresh)

# asenkron monitor korosu 
async def monitor(buffer, sample_counter):
    refresh_time = 0.1#second
    i=0
    while True: # infinite loop
        await asyncio.sleep(refresh_time)
        i+=refresh_time
        print(f"\rseconds: {i:2.1f}:: %Full: {buffer.qsize()*10:3}",
              f":: dropped: {sample_counter["dropped_packet_count"]}",
              f":: total: {sample_counter["total_packet_count"]}",
              end="")

# task cancel coro
async def cancel_task(task):
    task.cancel()
    # cancelled task must be awaited
    try:
        await task
    except asyncio.CancelledError:# cancel exception
        pass# no operation
    
# main coro
async def main():
    # buffer queue
    buffer           = asyncio.Queue(maxsize=10)
    acces_time       = 0.01#s
    snd_card_refresh = 0.1 #s
    # data statistics
    sample_counter   = {"dropped_packet_count":0, "total_packet_count":0}  
    
    print("SIMULATION IS STARTED!")

    # tasks created
    tasks = []
    # monitor task
    task  = asyncio.create_task(monitor(buffer, sample_counter))
    tasks.append(task)#0
    # harddisk data transfer task
    task  = asyncio.create_task(xmit(buffer, acces_time))
    tasks.append(task)#1
    # we wait for buffer to fill
    while not buffer.full():
        await asyncio.sleep(0.01)
    # soundcard data transfer task
    task = asyncio.create_task(recv(buffer, sample_counter, snd_card_refresh))
    tasks.append(task)#2
    
    # we cont. the sim. for a set period
    i=0
    while i<10:#s
        await asyncio.sleep(1)
        i+=1
    # 100 packets must be consumed by the soundcard at this point
    #print("::",i,"th second moment")# 10th second time 
    
    # tasks are cancelled
    # xmit task cancelled
    await cancel_task(tasks[1])
    
    # recv task will be cancelled
    # wait for queue to dry first
    
    #await asyncio.sleep(1)# stop delay
    #await buffer.join()   # may not operate correctly in case of a queue break
    # use this option to wait for draught of the queue
    while not buffer.empty():
        await asyncio.sleep(0.1)

    # recv task is cancelled
    await cancel_task(tasks[2])
    
    # final closing delay
    await asyncio.sleep(0.1)

    # monitor task is cancelled
    await cancel_task(tasks[0])
    
    print("\nSIMULATION IS STOPPED!")
          
# main PROGRAM BLOCK
if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    stop  = time.perf_counter()
    print(f"Total execution time:{stop - start : 2.3f} seconds.")