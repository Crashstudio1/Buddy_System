To simulate a Buddy System Memory Allocation algorithm, we can design and implement a Python module that includes the following functionalities:

Initialization: Define the total memory size and initialize the memory pool.
Allocation: Allocate memory using the Buddy System rules, finding the smallest available block size greater than or equal to the request.
Deallocation: Deallocate memory and merge adjacent free blocks if they form a "buddy."
Visualization: Display the current state of the memory pool for debugging and analysis.