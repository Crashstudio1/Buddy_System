# Buddy System Memory Allocation Simulator
from collections import defaultdict

class BuddySystem:
    def __init__(self, total_memory):                                           #initialize the memory size 2 to the power size
        if total_memory & (total_memory - 1) != 0:
            raise ValueError("Total memory size must be a power of 2.")

        self.total_memory = total_memory
        self.free_blocks = defaultdict(list)
        self.free_blocks[total_memory].append(0)
        self.allocated_blocks = {}

#allocate the processs
    def allocate(self, size):
        if size <= 0:
            raise ValueError("Requested size must be greater than 0.")               #check the process size
        block_size = 1
        while block_size < size:
            block_size *= 2
        for available_size in sorted(self.free_blocks.keys()):                      #check is there any available size
            if available_size >= block_size and self.free_blocks[available_size]:
                address = self.free_blocks[available_size].pop(0)
                while available_size > block_size:
                    available_size //= 2
                    buddy_address = address + available_size
                    self.free_blocks[available_size].append(buddy_address)
                self.allocated_blocks[address] = block_size
                return address, block_size
        raise MemoryError("Insufficient memory to allocate block.")

# Deallocate the process
    def deallocate(self, address, size):
        if size <= 0 or size & (size - 1) != 0:
            raise ValueError("Block size must be a power of 2.")
        if address not in self.allocated_blocks or self.allocated_blocks[address] != size:
            raise ValueError("Invalid deallocation: Block not found or size mismatch.")
        del self.allocated_blocks[address]
        block_size = size
        while block_size < self.total_memory:
            buddy_address = address ^ block_size
            if buddy_address in self.free_blocks[block_size]:
                self.free_blocks[block_size].remove(buddy_address)
                address = min(address, buddy_address)
                block_size *= 2
            else:
                break
        self.free_blocks[block_size].append(address)

    def display_memory(self):                                                       # Display the current memory state
        print("Current Memory State:")
        for size in sorted(self.free_blocks.keys(), reverse=True):
            for addr in self.free_blocks[size]:
                print(f"1 block of {size} KB (free at address {addr})")
        for addr, size in sorted(self.allocated_blocks.items()):
            print(f"1 block of {size} KB (allocated at address {addr})")

    def display_allocation_table(self):
        print("\nAllocation Table:")                                                #display the Allocation table
        print("+--------------------+----------------+")
        print("| Allocated Address  | Block Size (KB)|")
        print("+--------------------+----------------+")
        for addr, size in sorted(self.allocated_blocks.items()):
            print(f"| {addr:<18} | {size:<14} |")
        print("+--------------------+----------------+")

                                                                                    # Simulator Entry Point - Main Function
if __name__ == "__main__":
    print("Welcome to the Buddy System Memory Allocation Simulator")

    total_memory = int(input("Enter the total memory size (power of 2): "))
    buddy = BuddySystem(total_memory)

    process_sizes = []

    while True:
        print("\nOptions:")
        print("1. Add Process")
        print("2. Allocate Memory for Processes")
        print("3. Deallocate Memory")
        print("4. Display Memory State")
        print("5. Display Allocation Table")
        print("6. Exit")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            size = int(input("Enter process size: "))
            process_sizes.append(size)
            print(f"Process of size {size} added.")
        elif choice == 2:
            print("\nAllocation Results:")
            print("+---------+----------------+--------------------+----------------+-----------+")
            print("| Process | Requested Size | Allocated Address | Allocated Size | Waste     |")
            print("+---------+----------------+--------------------+----------------+-----------+")
            for i, size in enumerate(process_sizes, 1):
                try:
                    addr, alloc_size = buddy.allocate(size)
                    print(f"| {i:<7} | {size:<14} | {addr:<18} | {alloc_size:<14} | {alloc_size - size:<9} |")
                except MemoryError:
                    print(f"| {i:<7} | {size:<14} | {'Failed to allocate':<18} | {'-':<14} | {'-':<9} |")
            print("+---------+----------------+--------------------+----------------+-----------+")
            process_sizes = []
        elif choice == 3:
            addr = int(input("Enter starting address of the block to deallocate: "))
            size = int(input("Enter size of the block to deallocate: "))
            buddy.deallocate(addr, size)
        elif choice == 4:
            buddy.display_memory()
        elif choice == 5:
            buddy.display_allocation_table()
        elif choice == 6:
            break
        else:
            print("Invalid choice. Try again.")
