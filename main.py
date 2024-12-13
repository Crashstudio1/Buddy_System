from collections import defaultdict


class BuddySystem:
    def __init__(self, total_memory):
        """
        Initialize the buddy system with a given total memory size (in powers of 2).
        :param total_memory: Total memory size (must be a power of 2).
        """
        if total_memory & (total_memory - 1) != 0:
            raise ValueError("Total memory size must be a power of 2.")

        self.total_memory = total_memory
        self.free_blocks = defaultdict(list)  # Dictionary to store free blocks by size
        self.free_blocks[total_memory] = [0]  # Initially, the entire memory is free

    def allocate(self, size):
        """
        Allocate memory using the buddy system.
        :param size: Size of memory to allocate (rounded to the next power of 2).
        :return: The starting address of the allocated block and the actual block size allocated.
        """
        if size <= 0:
            raise ValueError("Requested size must be greater than 0.")

        block_size = 1
        while block_size < size:
            block_size *= 2

        for available_size in sorted(self.free_blocks.keys()):
            if available_size >= block_size and self.free_blocks[available_size]:
                address = self.free_blocks[available_size].pop(0)
                while available_size > block_size:
                    available_size //= 2
                    buddy_address = address + available_size
                    self.free_blocks[available_size].append(buddy_address)
                return address, block_size

        raise MemoryError("Insufficient memory to allocate block.")

    def deallocate(self, address, size):
        """
        Deallocate memory and merge buddies if possible.
        :param address: Starting address of the block to deallocate.
        :param size: Size of the memory block (must be a power of 2).
        """
        if size <= 0 or size & (size - 1) != 0:
            raise ValueError("Block size must be a power of 2.")

        block_size = size
        while block_size < self.total_memory:
            buddy_address = address ^ block_size  # Buddy address calculation using XOR
            # Try to merge with the smallest buddy available
            if buddy_address in self.free_blocks[block_size]:
                self.free_blocks[block_size].remove(buddy_address)
                address = min(address, buddy_address)  # Update the starting address to the lower one
                block_size *= 2  # Merge the blocks and increase the size
            else:
                break

        self.free_blocks[block_size].append(address)

    def display_memory(self):
        """
        Display the current state of memory.
        """
        print("Current Memory State:")
        for size, blocks in sorted(self.free_blocks.items()):
            print(f"Block Size {size}: {blocks}")


# Example usage of the optimized buddy system
if __name__ == "__main__":
    print("Welcome to the Buddy System Memory Allocation Simulator")

    try:
        total_memory = int(input("Enter the total memory size (power of 2): "))
        buddy = BuddySystem(total_memory)
    except ValueError as e:
        print(e)
        exit()

    process_sizes = []
    allocations = []

    while True:
        print("\nOptions:")
        print("1. Add Process")
        print("2. Allocate Memory for Processes")
        print("3. Display Memory State")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                size = int(input("Enter process size: "))
                if size > 0:
                    process_sizes.append(size)
                    print(f"Process of size {size} added.")
                else:
                    print("Process size must be greater than 0.")

            elif choice == 2:
                if not process_sizes:
                    print("No processes to allocate. Please add processes first.")
                    continue

                allocations = []
                for i, size in enumerate(process_sizes):
                    try:
                        address, allocated_size = buddy.allocate(size)
                        allocations.append((i + 1, size, address, allocated_size, allocated_size - size))
                    except MemoryError:
                        allocations.append((i + 1, size, None, None, None))

                print("\nAllocation Results:")
                print("+---------+----------------+--------------------+----------------+-----------+")
                print("| Process | Requested Size | Allocated Address | Allocated Size | Waste     |")
                print("+---------+----------------+--------------------+----------------+-----------+")
                for allocation in allocations:
                    proc, req_size, addr, alloc_size, waste = allocation
                    if addr is not None:
                        print(f"| {proc:<7} | {req_size:<14} | {addr:<18} | {alloc_size:<14} | {waste:<9} |")
                    else:
                        print(f"| {proc:<7} | {req_size:<14} | {'Not Allocated':<18} | {'-':<14} | {'-':<9} |")
                print("+---------+----------------+--------------------+----------------+-----------+")

            elif choice == 3:
                buddy.display_memory()

            elif choice == 4:
                print("Exiting the simulator. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"Error: {e}")
