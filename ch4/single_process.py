# this example shows that executing an arithmetic
# operation in a single process results to a low
# performance.

# time performance
import time

# process task
def task():
    # a complex calculation task is handled here
    for i in range(10**7):
        # a complex function
        p = ((((i+0.1)**2)/3.141)**2 + (i+1.2)*1.288**2)**0.5 - (25.5/(i-3.22))**1.148
        result[i] = p
        

if __name__ == '__main__':

    # start time
    start = time.perf_counter()
    
    # result data
    result = []
    [result.append(0) for _ in range(10**7)]

    task()
    stop = time.perf_counter()

    print(f"The calulation took {stop - start : 3.5f} seconds")

    print(result[0])
