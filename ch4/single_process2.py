# we divided the input data into intervals
# we used serail processing though

# time performance
import time

# process task
def task(intervals):
    # a complex calculation is made here
    for k in range(len(intervals)):
        for i in range(intervals[k][0], intervals[k][1]):
            # a complex function
            p = ((((i+0.1)**2)/3.141)**2 + (i+1.2)*1.288**2)**0.5 - (25.5/(i-3.22))**1.148
            result[i] = p
    
if __name__ == '__main__':

    # start time
    start = time.perf_counter()
    
    # results
    result = []
    [result.append(0) for _ in range(10**7)]

    # interval calculations
    intervals = []
    # interval count is set
    interval_count = 10
    interval = 10**7//interval_count
    for i in range(0, interval_count):
        intervals.append([i*interval, (i+1)*interval])
    
    task(intervals)
    stop = time.perf_counter()

    print(f"Calculation took {stop - start : 3.5f} seconds")

    print(result[0])
