import matplotlib
matplotlib.use('TkAgg')
import random
import matplotlib.pyplot as plt
import numpy as np

class CacheLine:
    def __init__(self, tag=None, data=None, state='I'):
        self.tag = tag  # Tag bits to identify memory block
        self.data = data  # Data stored in the cache line
        self.state = state  # Cache line state (M, E, S, I)

class Cache:
    def __init__(self, num_lines):
        self.num_lines = num_lines
        self.lines = [CacheLine() for _ in range(num_lines)]

    def read(self, address):
        pass  # Placeholder for read operation

    def write(self, address, data):
        pass  # Placeholder for write operation

    def invalidate(self, address):
        pass  # Placeholder for invalidate operation

class Memory:
    def __init__(self, size):
        self.size = size
        self.data = [0] * size  # Main memory contents

    def read(self, address):
        pass  # Placeholder for read operation

    def write(self, address, data):
        pass  # Placeholder for write operation

class Processor:
    def __init__(self, cache, memory):
        self.cache = cache
        self.memory = memory

    def read(self, address):
        pass  # Placeholder for read operation

    def write(self, address, data):
        pass  # Placeholder for write operation

class Bus:
    def __init__(self):
        pass

    def read(self, address):
        pass  # Placeholder for read operation

    def write(self, address, data):
        pass  # Placeholder for write operation

class MESIProtocol:
    def __init__(self):
        pass

    def handle_read(self, cache_line):
        pass  # Placeholder for handling read operation

    def handle_write(self, cache_line):
        pass  # Placeholder for handling write operation

    def handle_invalidate(self, cache_line):
        pass  # Placeholder for handling invalidate operation

def visualize_cache_state(cache):
    states = [line.state for line in cache.lines]
    labels = [f"Line {i}" for i in range(1, len(states) + 1)]
    colors = ['lightblue' if state == 'I' else 'lightgreen' if state == 'S' else 'lightgrey' for state in states]

    plt.figure(figsize=(8, 4))
    plt.bar(labels, [1] * len(states), color=colors)
    plt.title('Cache State')
    plt.xlabel('Cache Line')
    plt.ylabel('State')
    plt.show()

if __name__ == "__main__":
    # Initialize memory
    memory = Memory(size=16)

    # Initialize caches for 16 processors
    caches = [Cache(num_lines=4) for _ in range(16)]

    # Initialize processors with caches and memory
    processors = [Processor(cache, memory) for cache in caches]

    # Visualize initial cache state for processor 0
    visualize_cache_state(processors[0].cache)

