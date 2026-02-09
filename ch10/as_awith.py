# this example shows the use asynchronous with context
# to mmainge asynchronous web requests

# async io library
import asyncio
# time library
import time
# asynchronous web library
# use "python3 -m pip install aiohttp" to install
import aiohttp

# web status query task
async def web_status(web):
    # open client session first
    async with aiohttp.ClientSession() as session:
        # we get the status of the requested web site
        async with session.get(web) as result:
            return f"the status of the address({web}) ::: {result.status}"
    
# main coro
async def main():
    # web addresses
    webs = [
                # normal adresses produce "200:normal" code
                "http://www.sm0vpo.com/rx/tda7k-rx2.htm",
                "http://www.sm0vpo.com/rx/tba120-1.htm",
                "http://www.sm0vpo.com/rx/tda7000.htm",
                "http://www.sm0vpo.com/rx/quickrx.htm",
                "http://www.sm0vpo.com/rx/synth.htm",
                "http://www.elektormagazine.com/",
                # "404:not found" 
                "http://www.sm0vpo.com/rx/books.html",
                # wrong link address
                "http://www.elektormagazin.com/"
                
                ]
    print("\nWeb addresses status requested...")
    # start time
    start = time.perf_counter()
    # tasks are created and waited
    g = await asyncio.gather(*(web_status(web) for web in webs), return_exceptions=True)
    # results are reported
    for msg in g:
        print(msg)
    # stop time
    stop = time.perf_counter()
    print(f"\nexecution time:{stop-start:2.3f} seconds")
    
# main program block
if __name__ == "__main__":
    asyncio.run(main())
    