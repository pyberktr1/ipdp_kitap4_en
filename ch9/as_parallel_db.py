# this example shows the operation of a parallel database
# using asynchronous tasks

# async io library
import asyncio
# time library
import time
# random number library 
import random

# used in the query coro
time_out = 5.0# query time out limit (seconds)
# used in the search_task coro to simulate a fault
fault   = None#667# faulty serial number to be queried
# database {seri_no: [name, stock, cost]}
db = {
        311  : ["fuse   ", 33, 1.23],
        124  : ["diode  ", 13, 2.21],
        822  : ["coil   ", 25, 1.55],
        314  : ["switch ", 45, 6.73],
        525  : ["bulb   ", 83, 4.04],
        404  : ["relay  ", 66, 5.31],
        667  : ["cable  ", 71, 2.15],
        767  : ["module ", 58, 3.45],
        333  : ["pump   ", 11, 8.95]
          }

# main coro
async def main():
    # query queue
    query = asyncio.Queue()
    # result queue
    result = asyncio.Queue()
    # query list 3 out of 12 is faulty
    queries = [
                311, 124, 503,
                822, 314, 213,
                525, 404, 876,
                667, 767, 333
                ]
    print("***** SEARCHING STARTS *****")            
    # start time
    start = time.perf_counter()
    # tasks are created
    db_tasks = [] # db gorevleri
    for i in range(3):
        g = asyncio.create_task(data(i, query, result))
        db_tasks.append(g)
    # we use gather() for joining awaits
    try:
        await asyncio.gather(
              search_task(query, result, queries, db_tasks),
              *db_tasks, return_exceptions=False
                )
    # if one of the tasks are cancelled the others are also
    # cancelled automatically
    except* asyncio.CancelledError:# iptal istisnasi olustu
        pass# no operation
        
    # stop time
    stop = time.perf_counter()
    print("***** SEARCHING STOPS *****")            
    print(f"Total execution time: {stop - start:2.3f} seconds.")

# search_task coro
async def search_task(query, result, queries, db_tasks):

    # send all queries
    for q in queries:
        await query.put(q)
    
    # send cancel signal to all db_tasks 
    for _ in range(3):
        await query.put(None)
        
    # get all the results and report
    print()
    print("****** SEARCH RESULTS ******")
    print("----------------------------" 
          "----------------------------")

    # closed db tasks count
    closed = 0
    
    # infinite loop
    while True:
        
        # start time recorded for time out check
        start = time.perf_counter()
        
        # test result queue for emptiness
        while result.empty():
            await asyncio.sleep(0.1)
            # check timeout
            if (round(time.perf_counter()-start,1) > time_out):
                print("\033[91mtimedout when searching!\033[0m")
                print("\033[91mAll dbs will be closed!\033[0m")
                # cancel all db tasks
                for i in range(3):
                    if not db_tasks[i].done():
                        db_tasks[i].cancel()
                # after all db tasks are closed 
                # search task will be closed also
        
        # there is a new result in the queue
        res = await result.get()
        # is result valid?
        if res[1]==None:# related db is closed
            closed+=1
            print(f"\033[93mDB#{res[0]} is closed!\033[0m")
            print("----------------------------" 
                  "----------------------------")
            if closed==3:# all db_tasks are closed
                print("\033[92mAll queries are completed!\033[0m")
                break
        elif res[2]==None:# faulty serial number
            print(f"\033[91mdb:{res[0]}, could not find serial number:{res[1]}  | "
                  f"time:{res[3]}s\033[0m")
            print("----------------------------" 
                  "----------------------------")
        else:# there is a valid query result
            # report results
            print(f"db:{res[0]} :: part data for {res[1]}:")
            print(f"name:{res[2][0]} | stock:{res[2][1]} | "
                  f"cost=${res[2][2]} | time:{res[3]}s")
            print("----------------------------" 
                  "----------------------------")
                  
    print()
    print("***** END OF SEARCH RESULTS *****")
    
# database coro
async def data(i, query, result):         
    # infinite loop   
    while True:
        # check query queue
        while query.empty():
            await asyncio.sleep(0.1)
        
        # there is a new query in the queue
        search_no = await query.get()
        # if requested query is "None" then close the database task
        if search_no is None:
            break
        #print(f"fetching part data for serial number {search_no}...")
        # process delay
        opd = random.uniform(1, 2)
        await asyncio.sleep(opd)
        
        # simulate a fault in the database
        if search_no==fault:
            await asyncio.sleep(20)
        
        # is serial in the database?
        if search_no in db:
            #print(f"the part {search_no} has been found. time:{opd:2.3f}s")
            # throw the result to the output queue
            await result.put([i, search_no, db[search_no], round(opd,3)])
        else:
            #print(f"the part serial = {search_no} is wrong! time:{opd:2.3f}s")
            # put the result into output queue
            await result.put([i, search_no, None, round(opd,3)])
            
    # data server is being closed
    #print(f"the db#{i} will be closed...")
    await asyncio.sleep(0.1)
    await result.put([i, None, None, None])# report the closing to the search task

# main program bolumu
if __name__ == "__main__":
    asyncio.run(main())