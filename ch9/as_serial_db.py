# this example shows the operation of a serial database
# using asynchronous tasks

# async io library
import asyncio
# time library
import time
# random number library 
import random

# main coro
async def main():
    # part serials that will be queried
    # serial 11 is non-existent in the db
    serials = [3, 7, 13, 23, 33, 11]
    # start time
    start = time.perf_counter()
    # queries are started
    s = await asyncio.gather(*(get_data(serial) for serial in serials))
    # stop time
    stop = time.perf_counter()
    
    # final report
    print()
    print("***** QUERY RESULTS *****")
    print(f"{len(s)} queries resulted in",
          f" {stop - start:2.3f} seconds")
    print()
    print("***** START OF REPORT *****")
    print("-------------------------------------" 
          "-------------------------------------")
    for i in range(len(s)):
        # REPORT THE RESULTS
        print(f"the part with serial number {s[i]["serial"]} :")
        print(f"name:{s[i]["name"]} | stock_no:{s[i]["stock_no"]} | "
              f"stock:{s[i]["stock"]} | "
              f"stock_code:{s[i]["stock_code"]} | cost=${s[i]["cost"]}")
        print("-------------------------------------" 
              "-------------------------------------")
    print("***** END OF REPORT *****")

# data query
async def get_data(serial):
    # this query fetches the name
    stock_no , name   = await name_getir(serial)
    # this query fetches the stock data
    stock_code, stock = await stock_getir(stock_no)
    # this query fetches the cost
    cost              = await cost_getir(stock_code)
    
    return {"serial":serial, "name":name, 
            "stock_no":stock_no, "stock_code":stock_code,
            "stock":stock, "cost":cost}
    
# part name queries
async def name_getir(serial):
    # database {serial: [stock_no,name]}
    db = {
          3  : [1233, "fuse   "],
          7  : [1234, "diode  "],
          13 : [1235, "coil   "],
          23 : [1236, "switch "],
          33 : [1237, "bulb   "]
          }
          
    # process delay
    i = random.uniform(1.0, 2.0)
    print(f"{serial=} searched for part name...")
    await asyncio.sleep(i)
    if serial in db:
        print(f"part name of {serial=} fetched. time:{i:2.3f}s")
        return db[serial]
    else:
        print(f"{serial=}  is wrong! time:{i:2.3f}s")
        return [None, None]

# part stock queries
async def stock_getir(stock_no):
    # database {stock_no: [stock_code,stock]}
    db = {
          1233 : [313, 51],
          1234 : [525, 25],
          1235 : [373, 75],
          1236 : [555, 13],
          1237 : [741, 43]
          }
          
    # process delay
    i = random.uniform(1.0, 2.0)
    print(f"{stock_no=} searched for stock data...")
    await asyncio.sleep(i)
    if stock_no in db:
        print(f"{stock_no=} part stock data fetched. time:{i:2.3f}s")
        return db[stock_no]
    else:
        print(f"{stock_no=} is wrong! time:{i:2.3f}s")
        return [None, None]

# part cost queries
async def cost_getir(stock_code):
    # database {stock_code : cost}
    db = {
          313: 3.51,
          525: 2.15,
          373: 1.65,
          555: 8.23,
          741: 9.83
          }
          
    # process delay
    i = random.uniform(1.0, 2.0)
    print(f"{stock_code=} searched for part cost...")
    await asyncio.sleep(i)
    if stock_code in db:
        print(f"{stock_code=} part cost fetched. time:{i:2.3f}s")
        return db[stock_code]
    else:
        print(f"{stock_code=} is wrong! time:{i:2.3f}s")
        return None

# main program block
if __name__ == "__main__":
    asyncio.run(main())
    