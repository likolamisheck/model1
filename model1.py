import tkinter as tk
import random
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

# Constants
NUM_PROCESSORS = 4
MEMORY_SIZE = 16
CACHE_LINE_SIZE = 1
NUM_CACHE_LINES = 4
ASSOCIATIVITY = 2
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400

# Cache line states
STATE_INVALID = 'I'
STATE_SHARED = 'S'
STATE_EXCLUSIVE = 'E'
STATE_MODIFIED = 'M'
STATE_OWNED = 'O'

# Class to represent a cache line
class CacheLine:
    def __init__(self, tag=None, data=None, state=STATE_INVALID, last_access_time=0):
        self.tag = tag
        self.data = data
        self.state = state
        self.last_access_time = last_access_time

# Class to represent the cache
class Cache:
    def __init__(self, num_lines):
        self.num_lines = num_lines
        self.lines = [CacheLine() for _ in range(num_lines)]

    def read(self, address):
        pass # Placeholder for read operation

    def write(self, address, data):
        pass # Placeholder for write operation

    def invalidate(self, address):
        pass # Placeholder for invalidate operation

# Class to represent the memory
class Memory:
    def __init__(self, size):
        self.size = size
        self.data = [0] * size  # Main memory contents

    def read(self, address):
        pass  # Placeholder for read operation

    def write(self, address, data):
        pass  # Placeholder for write operation

# Class to represent the processor
class Processor:
    def __init__(self, cache, memory):
        self.cache = cache
        self.memory = memory

    def read(self, address):
        pass  # Placeholder for read operation

    def write(self, address, data):
        pass  # Placeholder for write operation

# Class to represent the bus
class Bus:
    def __init__(self):
        pass

    def read(self, address):
        pass  # Placeholder for read operation

    def write(self, address, data):
        pass  # Placeholder for write operation

# Class to implement the MOESI protocol
class MOESIProtocol:
    def __init__(self):
        pass

    def handle_read(self, cache_line):
        pass  # Placeholder for handling read operation

    def handle_write(self, cache_line):
        pass  # Placeholder for handling write operation

    def handle_invalidate(self, cache_line):
        pass  # Placeholder for handling invalidate operation

def visualize_cache_state(cache, figure):
    states = [line.state for line in cache.lines]
    labels = [f"Line {i}" for i in range(1, len(states) + 1)]
    colors = ['lightblue' if state == 'I' else 'lightgreen' if state == 'S' else 'lightgrey' for state in states]
    figure.clear()
    ax = figure.add_subplot(111)
    ax.bar(labels, [1] * len(states), color=colors)
    ax.set_title('Cache State')
    ax.set_xlabel('Cache Line')
    ax.set_ylabel('State')

class SimulationGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cache Simulation")
        self.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT + 200}")

        # Initialize components
        self.memory = Memory(size=16)
        self.caches = [Cache(num_lines=4) for _ in range(4)]
        self.processors = [Processor(cache, self.memory) for cache in self.caches]
        self.moesi_protocol = MOESIProtocol()

        # Create GUI elements
        self.create_widgets()
        self.draw_initial_state()

    def create_widgets(self):
        # Create a canvas for animation
        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)

        # Create a frame for controls
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        # Add controls for read/write operations
        operation_label = tk.Label(control_frame, text="Operation:")
        operation_label.pack(pady=5)

        self.operation_var = tk.StringVar()
        self.operation_var.set("read")
        read_radio = tk.Radiobutton(control_frame, text="Read", variable=self.operation_var, value="read")
        read_radio.pack(pady=5)
        write_radio = tk.Radiobutton(control_frame, text="Write", variable=self.operation_var, value="write")
        write_radio.pack(pady=5)

        # Add controls for processor selection
        processor_label = tk.Label(control_frame, text="Processor:")
        processor_label.pack(pady=5)

        self.processor_var = tk.IntVar()
        self.processor_var.set(0)
        for i in range(4):
            processor_radio = tk.Radiobutton(control_frame, text=f"Processor {i}", variable=self.processor_var, value=i)
            processor_radio.pack(pady=5)

        # Add controls for memory address
        address_label = tk.Label(control_frame, text="Memory Address:")
        address_label.pack(pady=5)

        self.address_entry = tk.Entry(control_frame)
        self.address_entry.pack(pady=5)

        # Add a button to perform the operation
        perform_button = tk.Button(control_frame, text="Perform Operation", command=self.perform_operation)
        perform_button.pack(pady=10)

        # Add a canvas for cache state visualization
        self.cache_figure = plt.figure(figsize=(4, 2.5))
        self.cache_canvas = FigureCanvasTkAgg(self.cache_figure, master=self)
        self.cache_canvas.get_tk_widget().pack(side=tk.BOTTOM, padx=10, pady=10)

    def draw_initial_state(self):
        # Clear the animation canvas
        self.canvas.delete("all")

        # Draw the initial state of the system
        self.draw_memory()
        self.draw_bus()
        self.draw_processors()

        # Visualize the initial cache state
        visualize_cache_state(self.processors[0].cache, self.cache_figure)
        self.cache_canvas.draw()

    def draw_memory(self):
        # Draw the memory
        memory_x = 50
        memory_y = 50
        memory_width = 100
        memory_height = 300
        self.canvas.create_rectangle(memory_x, memory_y, memory_x + memory_width, memory_y + memory_height, fill="lightgray")
        self.canvas.create_text(memory_x + memory_width // 2, memory_y + 15, text="Memory")

    def draw_bus(self):
        # Draw the bus
        bus_x1 = 200
        bus_x2 = CANVAS_WIDTH - 200
        bus_y = CANVAS_HEIGHT // 2
        self.canvas.create_line(bus_x1, bus_y, bus_x2, bus_y, width=3)
        self.canvas.create_text((bus_x1 + bus_x2) // 2, bus_y - 15, text="Bus")

    def draw_processors(self):
        # Draw the processors
        processor_width = 100
        processor_height = 150
        processor_spacing = (CANVAS_WIDTH - 200 - 4 * processor_width) // 