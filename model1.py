import tkinter as tk
import random
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import time
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
        tag, index = divmod(address, NUM_CACHE_LINES)
        for line in self.lines:
            if line.tag == tag:
                line.last_access_time = time.time()
                return line.data
        # Cache miss, implement random replacement
        random_index = random.randint(0, self.num_lines - 1)
        self.lines[random_index].tag = tag
        self.lines[random_index].data = 'Data from memory'
        self.lines[random_index].last_access_time = time.time()
        return self.lines[random_index].data

    def write(self, address, data):
        tag, index = divmod(address, NUM_CACHE_LINES)
        for line in self.lines:
            if line.tag == tag:
                line.data = data
                line.state = STATE_MODIFIED
                line.last_access_time = time.time()
                return
        # Cache miss, implement random replacement
        random_index = random.randint(0, self.num_lines - 1)
        self.lines[random_index].tag = tag
        self.lines[random_index].data = data
        self.lines[random_index].state = STATE_MODIFIED
        self.lines[random_index].last_access_time = time.time()

    def invalidate(self, address):
        tag, index = divmod(address, NUM_CACHE_LINES)
        for line in self.lines:
            if line.tag == tag:
                line.state = STATE_INVALID
                return

    def get_tag(self, address):
        # Extract tag from the memory address
        return address // CACHE_LINE_SIZE

    def find_cache_line(self, tag):
        # Find the cache line with the given tag
        for line in self.lines:
            if line.tag == tag:
                return line
        return None

    def handle_cache_miss(self, address, tag, is_read):
        # Handle cache miss by randomly replacing a cache line
        victim_line = random.choice(self.lines)
        if victim_line.state == STATE_MODIFIED:
            # Write back the modified data to memory
            self.memory.write(victim_line.tag * CACHE_LINE_SIZE, victim_line.data)
        victim_line.tag = tag
        victim_line.data = self.memory.read(address)
        if is_read:
            victim_line.state = STATE_SHARED
            self.moesi_protocol.handle_read(victim_line)
        else:
            victim_line.state = STATE_MODIFIED
            self.moesi_protocol.handle_write(victim_line)
# Class to represent the memory
class Memory:
    def __init__(self, size):
        self.size = size
        self.data = [0] * size  # Main memory contents

    def read(self, address):
        # Implement read operation
        return self.data[address]

    def write(self, address, data):
        # Implement write operation
        self.data[address] = data

# Class to represent the processor
class Processor:
    def __init__(self, cache, memory):
        self.cache = cache
        self.memory = memory

    def read(self, address):
        # Implement read operation according to MOESI protocol
        self.cache.read(address)

    def write(self, address, data):
        # Implement write operation according to MOESI protocol
        self.cache.write(address, data)

# Class to represent the bus
class Bus:
    def __init__(self):
        pass

    def read(self, address):
        # Implement read operation
        pass

    def write(self, address, data):
        # Implement write operation
        pass

# Class to implement the MOESI protocol
class MOESIProtocol:
    def __init__(self):
        pass

    def handle_read(self, cache_line):
        # Implement handling of read operation according to MOESI protocol
        if cache_line.state == STATE_INVALID:
            cache_line.state = STATE_SHARED
        elif cache_line.state == STATE_EXCLUSIVE:
            cache_line.state = STATE_SHARED
        elif cache_line.state == STATE_MODIFIED:
            cache_line.state = STATE_OWNED
        # Update other cache lines as needed

    def handle_write(self, cache_line):
        # Implement handling of write operation according to MOESI protocol
        if cache_line.state == STATE_INVALID:
            cache_line.state = STATE_MODIFIED
        elif cache_line.state == STATE_SHARED:
            cache_line.state = STATE_MODIFIED
            # Invalidate other shared copies
        elif cache_line.state == STATE_EXCLUSIVE:
            cache_line.state = STATE_MODIFIED
        elif cache_line.state == STATE_OWNED:
            cache_line.state = STATE_MODIFIED
            # Invalidate other shared copies

    def handle_invalidate(self, cache_line):
        # Implement handling of invalidate operation according to MOESI protocol
        pass

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
        self.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT + 300}")  # Increased height

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

        # Create a separate canvas for the output text box
        self.output_canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=100, bg="white")
        self.output_canvas.pack(side=tk.TOP, padx=10, pady=10)

        # Create a text box on the output canvas for displaying output
        self.output_textbox = self.output_canvas.create_text(20, 20, anchor="nw", font=("Arial", 12), text="Output:")

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
            

    def perform_operation(self):
        operation = self.operation_var.get()
        processor_index = self.processor_var.get()
        address_input = self.address_entry.get()

    # Check if the address input is a valid integer
        try:
            address = int(address_input)
            if not 0 <= address <= 15:
                raise ValueError("Address must be between 0 and 15")
        except ValueError:
            output_text = "Invalid memory address! Please enter a valid number between 0 and 15."
            self.output_canvas.itemconfigure(self.output_textbox, text=f"Output: {output_text}")
            return

    # Perform the operation based on the selected operation type
        if operation == "read":
            data = self.processors[processor_index].read(address)
            output_text = f"Processor {processor_index} reading from address {address}, Data: {data}, Cache State: {[line.state for line in self.processors[processor_index].cache.lines]}"
        elif operation == "write":
            data = random.randint(0, 255)
            self.processors[processor_index].write(address, data)
            output_text = f"Processor {processor_index} writing {data} to address {address}, Cache State: {[line.state for line in self.processors[processor_index].cache.lines]}"

    # Update the output text on the output canvas
        self.output_canvas.itemconfigure(self.output_textbox, text=f"Output: {output_text}")
        
        
      #   Check for cache coherence events
        events = []
        for i, processor in enumerate(self.processors):
            if i != processor_index:
                other_cache_state = [line.state for line in processor.cache.lines]
                for j, line_state in enumerate(other_cache_state):
                    if line_state == 'M':
                        events.append(f"Processor {processor_index} invalidated line {j} in Processor {i}'s cache.")
                        processor.cache.lines[j].state = 'I'

    # Update the output text on the output canvas
        output_text += '\n' + '\n'.join(events)
        self.output_canvas.itemconfigure(self.output_textbox, text=f"Output: {output_text}")
        
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
        bus_x1 = 50 + 100  # Adjusted to the center of memory
        bus_x2 = 200 + 3 * (100 + (CANVAS_WIDTH - 200 - 4 * 100) // 3) + 100 // 2  # Adjusted to CPU 3
        bus_y = CANVAS_HEIGHT // 2
        self.canvas.create_line(bus_x1, bus_y, bus_x2, bus_y, width=3)
        self.canvas.create_text((bus_x1 + bus_x2) // 2, bus_y - 15, text="Bus")

    def draw_processors(self):
    # Draw the processors
        processor_width = 100
        processor_height = 150
        processor_spacing = (CANVAS_WIDTH - 200 - 4 * processor_width)
        processor_y = CANVAS_HEIGHT // 4
        cpu_coords = []  # Store CPU coordinates for connecting lines
        for i in range(4):
            processor_x = 200 + i * (processor_width + processor_spacing // 3)
            self.canvas.create_rectangle(processor_x, processor_y, processor_x + processor_width, processor_y + processor_height, fill="lightblue")
            self.canvas.create_text(processor_x + processor_width // 2, processor_y + processor_height // 2, text=f"Processor {i}")
            cpu_coords.append((processor_x + processor_width // 2, processor_y + processor_height // 2))


    def draw_cache(self):
        pass  # Placeholder for drawing cache visualization
if __name__ == "__main__":
    root = SimulationGUI()
    root.mainloop()
