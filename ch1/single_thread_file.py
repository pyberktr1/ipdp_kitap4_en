# sample application for serial file processing

# time performance
from time import perf_counter
# module for test file initialization
import test_file

# file task
def exchange(file, search_text, replace_text):
    print(f"File {file} opened for process\n", end="")
        
    # file is opened for reading
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
    # files created
    files = []

    for i in range (1,11):
        files.append(f"./files/test{i}.txt")
    
    # search text exchanged
    for file in files:
        exchange(file, 'bir', '***ÜÇ***')

# __main__ name space is used to call the main program block
# direct execution puts the below code to execution
# when it is imported as a module, below code part is not executed
if __name__ == "__main__":
    
    # test files initialized
    test_file
    
    # start time
    start = perf_counter()
    # call to main program block
    main()
    # stop time
    stop = perf_counter()
    print(f'Execution took {stop - start :2.5f} seconds.')
