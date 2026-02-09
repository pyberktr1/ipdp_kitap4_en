# using Thread class for thread operations
# threading library
from threading import Thread

# thread class is re-arranged
# a new thread class is defined to make file read operations
class thread_file_read(Thread):
    # initialization body
    def __init__(self, file: str) -> None:
        super().__init__()
        self.file   = file                       # file name
        self.line   = ""                         # file data
        self.status = "File read is succesful"   # file reading status
    # execution body
    def run(self) -> None:
        print(f"{self.file} is reading...\n", end="")
        try:
            with open(self.file, 'r') as f:
                self.line = f.read()
        except FileNotFoundError as err:
            self.status = f"ERROR!: {self.file} not found!"
        except IOError as err:
            self.status = f"ERROR!: {self.file} I/O error!"

# main program block
def main() -> None:
    # file data to be read
    files = [
        "./files/text1.txt",
        "./files/text2.txt"
    ]

    # threads created
    threads = [thread_file_read(file) for file in files]

    # threads started
    [thread.start() for thread in threads]

    # wait for threads to complete
    [thread.join() for thread in threads]

    # display each file content
    [print(f"{thread.file} : \n{thread.line} :: file status: {thread.status}") 
        for thread in threads]
# call to main
if __name__ == "__main__":
    main()
    
