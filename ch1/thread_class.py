# using Thread class for thread operations
# threading library
from threading import Thread

# thread class is re-arranged
# a new thread class is defined to make file write operations
class thread_file_write(Thread):
    # initialization body
    def __init__(self, file: str, line:str) -> None:
        super().__init__()
        self.file  = file   # file name
        self.line  = line   # file data
    # execution body
    def run(self) -> None:
        print(f"{self.file} writing...\n", end="")
        with open(self.file, 'a') as f:
            f.write(self.line)

# main program block
def main() -> None:
    # file data to be written
    data = [
        ["./files/text1.txt", "QUICK BROWN FOX\n"],
        ["./files/text2.txt", "JUMPS OVER LAZY DOG\n"]
    ]
    
    # threads created
    threads = [thread_file_write(file, line) for [file, line] in data]
    # threads starts
    [thread.start() for thread in threads]
    # threads are waited
    [thread.join() for thread in threads]

    print("All file writes complete!")

# call to main
if __name__ == "__main__":
    main()
    
