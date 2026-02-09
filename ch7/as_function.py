# this example shows the differences between
# synchronous and asynchronous functions
# (co-routine of coro in short).

# async I/O library
import asyncio

# a normal (synchronous) function definition
def cube(number: int) -> int:
    # cube of a number 
    return number**3

# the asynchronous function (coro) definition
# that does the same job as above function   
async def as_cube(number: int) -> int:
    return number**3

# main program block
if __name__ == '__main__':
    # synchronous function call
    res=cube(2)
    print(f"synchronous result: {res}")
    print()
    
    # simple asynchronous function call, 
    # just returns a coro object
    res=as_cube(2)
    print(f"coro object: {res}")
    
    # direct asynchronous function call
    # asyncio.run() can be used only
    # for coros and only once
    res=asyncio.run(as_cube(2))
    print()
    # result of the actual coro execution
    print(f"asynchronous result: {res}")
        
