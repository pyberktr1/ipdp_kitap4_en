# sample application for working with multi-threaded files

# performance display
from time import perf_counter, sleep
# module for preparing test files
import test_file
# thread library
from threading import Thread

# file task
def exchange(file, search_text, replace_text):
    print(f"File {file} opened for process\n", end="")
    
    # We can block one of the duties by activating
    # below code block.    
    # (put a "#" in front of the first line for activation)
    """
    if (file == "./file/test3.txt"):
        sleep(3)
        #"""
        
    # file is openede for reading
    with open(file, 'rb') as f:
        data = f.read()
    # byte data is changed to text data 
    text = data.decode('utf-8')
    
    # search in progress
    i = 0
    start = 0
    while (found := text.find(search_text, start)) != -1:
        i += 1
        start = found + 1
        
    print(f"{file} has --{search_text}-- text in {i} places. \n", end="")
    
    # exchange in progress
    text = text.replace(search_text, replace_text)

    # text is converted to byte data for writing to the file
    with open(file, 'wb') as f:
        f.write(text.encode('utf-8'))
        
    print(f"{file} is complete \n", end="")

# main program block
def main():
    # test files are prepared
    test_file
   
   # file names
    files = []

    for i in range (1,11):
        files.append(f"./files/test{i}.txt")

    # threads are created
    threads = [Thread(target=exchange, args=(file, 'bir', '***ÜÇ***'))
            for file in files]

    # start time
    start = perf_counter()
    
    # start threads
    for thread in threads:
        thread.start()

    # thread start time
    th_st = perf_counter()

    # wait for all file tasks to end
    for thread in threads:
        thread.join()

    # stop time   
    stop = perf_counter()

    # results
    print(f"\n thread starting : {th_st - start :2.5f} saniye",
          f"\n thread tasks    : {stop - th_st  :2.5f} saniye",
          f"\n total           : {stop - start  :2.5f} saniye")
    
    print("Press Enter to finish...")
    input()

# __main__ namespace is used to call the main program block
if __name__ == "__main__":
    
    # call to the main program block
    main()
