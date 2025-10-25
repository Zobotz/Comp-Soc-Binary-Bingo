import tkinter as tk
import random
import time
from threading import Thread

# Global variables  
# Colours
PURPLE = "#ae46ea"
TEAL = "#28d6a9"
BG_COLOR = "#1a1a1a"
font = "Helvetica"
# linked list
list_size = 0
head = None
# buttons
next_pressed = False
started = False
# banner
called_numbers = []
speed = 3  # pixels per frame for banner scroll
font = ("Arial", 48, "bold")
gap_text = "     "  # gap after the number list in banner
banner_text = ""
banner_height = 80

# Setting up linked list
# ensures no duplicate numbers
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def setInitalList():
    global head, list_size
    list_size = 0
    head = None
    last = None
    for x in range(67):
        newNode = Node(x)
        if head == None:
            head = newNode
        else:
            last.next = newNode
        last=newNode
        list_size+=1
    
    for x in range(61):
        i = x+68
        newNode = Node(i)
        if head == None:
            head = newNode
        else:
            last.next = newNode
        last=newNode
        list_size+=1

    return head

# colours done on gradient
def hex_to_rgb(hex_color):
    # Convert hex string (#rrggbb) to an RGB tuple
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    # Convert an RGB tuple to a hex string
    return "#%02x%02x%02x" % rgb

def choose_colour(start_hex, end_hex, factor):
    # Blend two hex colours by factor (0.0–1.0).
    # 0.0 = start colour, 1.0 = end colour.
    start = hex_to_rgb(start_hex)
    end = hex_to_rgb(end_hex)
    r = int(start[0] + (end[0] - start[0]) * factor)
    g = int(start[1] + (end[1] - start[1]) * factor)
    b = int(start[2] + (end[2] - start[2]) * factor)
    return rgb_to_hex((r, g, b))

# Random binary generator
def random_binary():
    global list_size, head
    if list_size==0:
        return 128, 10000000
 
    # randomly chooses the linked list position
    index = random.randint(0, list_size-1)

    prev=None
    current=head

    # locates the random number in linked list
    for i in range(index):
        prev = current
        current = current.next

    number = current.data
    binary = format(number, "08b")

    # removes chosen number from linked list
    if prev == None:
        head = current.next
    else:
        prev.next = current.next
    list_size -=1

    return number, binary

def show_number():
    global next_pressed, started, running
    if not running or not started:
        window.after(100, show_number)
        return

    if not next_pressed:
        window.after(100, show_number)
        return

    next_pressed = False

    number, binary = random_binary()
    print(number)

    factor = number / 127
    colour = choose_colour(TEAL, PURPLE, factor)

    # Show binary first
    label.config(text=binary, fg=PURPLE)

    # After 3 seconds, show decimal
    # inside show_number() because it allows sharing of local variables without passing
    def show_decimal():
        label.config(text=str(number), fg=colour)
        called_numbers.insert(0, number)
        update_banner_text()
        window.after(100, show_number)  # schedule next cycle safely

    window.after(3000, show_decimal) # miliseconds for delay after binary number


# buttons functions
def start_program():
    global started
    started = True
    start_button.config(state="disabled")  # disable start after pressing

def next_number():
    global next_pressed
    next_pressed = True

def restart_program():
    global started, called_numbers
    setInitalList()
    started = False
    called_numbers.clear()
    label.config(text="Press Start", fg=PURPLE)
    start_button.config(state="normal")
    reset_banner_position()
    update_banner_text()

# set up the linked list before starting
head = setInitalList()
current=head

# create window
window = tk.Tk()
window.title("Binary Display with Bingo Banner")
window.geometry("800x350") # increased height for banner + main display
window.configure(bg=BG_COLOR)

# Banner Canvas
banner_canvas = tk.Canvas(window, width=800, height=banner_height, bg="black", highlightthickness=0)
banner_canvas.pack(side="top", fill="x")
banner_canvas.update()
canvas_width = banner_canvas.winfo_width()
text_item = banner_canvas.create_text(
    canvas_width,
    banner_height // 2,
    text=banner_text,
    font=font,
    fill=TEAL,
    anchor="w"
)
# Create banner text item
banner_text = "Waiting for numbers..." + gap_text
text_item = banner_canvas.create_text(
    1500,                    
    banner_height // 2,
    text=banner_text,
    font=font,
    fill=TEAL,
    anchor="w"
)
banner_canvas.update()
text_width = banner_canvas.bbox(text_item)[2] - banner_canvas.bbox(text_item)[0]
# Banner scroll logic# Start banner scrolling
def move_banner():
    global text_width
    for item in text_items:
        banner_canvas.move(item, -speed, 0)
    # When text leaves the screen, restart
    x = banner_canvas.coords(text_items[0])[0]
    if x + text_width < 0:
        banner_canvas.coords(text_items[0], 1500, banner_height // 2)
    window.after(20, move_banner)

def update_banner_text():
    global text_width, text_items
    banner_canvas.delete("all")  # clear existing text

    text_items = []
    x = 1500  # starting x position
    y = banner_height // 2

    if called_numbers:
        # Create each number with colour based on its value
        for num in called_numbers:
            factor = num / 127
            color = choose_colour(TEAL, PURPLE, factor)
            item = banner_canvas.create_text(
                x, y,
                text=str(num),
                font=font,
                fill=color,
                anchor="w"
            )
            bbox = banner_canvas.bbox(item)
            width = bbox[2] - bbox[0] + 20  # small gap between numbers
            x += width
            text_items.append(item)
    else:
        # Default message
        item = banner_canvas.create_text(
            x, y,
            text="Waiting for numbers...",
            font=font,
            fill=TEAL,
            anchor="w"
        )
        text_items.append(item)

    # Compute banner width for reset logic
    banner_canvas.update()
    bbox = banner_canvas.bbox(text_items[-1])
    text_width = bbox[2] - banner_canvas.bbox(text_items[0])[0]
    banner_canvas.coords(text_items[0], 1500, y)

def reset_banner_position():
    # Reset banner to start at right edge
    banner_canvas.coords(text_item, 800, banner_height//2)

# Close safely on exit
def on_close():
    global running
    running = False
    window.destroy()

# Text label for binary/decimal
label = tk.Label(
    window,
    text="",
    font=(font, 200, "bold"), # font and size of text
    bg=BG_COLOR,
    fg=PURPLE
)
label.pack(expand=True)

# Buttons
button_frame = tk.Frame(window, bg=BG_COLOR)
button_frame.pack(pady=20)

start_button = tk.Button(button_frame, text="Start", command=start_program, font=(font, 16), bg=PURPLE)
start_button.grid(row=0, column=0, padx=10)

next_button = tk.Button(button_frame, text="Next", command=next_number, font=(font, 16), bg = '#6b8eca')
next_button.grid(row=0, column=1, padx=10)

restart_button = tk.Button(button_frame, text="Restart", command=restart_program, font=(font, 16), bg=TEAL)
restart_button.grid(row=0, column=2, padx=10)

# credit label (placed bottom-right)
label1 = tk.Label(
    window,
    text="Code by Zoe Weston",
    font=(font, 10, "bold"),
    bg=BG_COLOR,
    fg=TEAL
)
label2 = tk.Label(window,
    text="And Isabelle Wickens",
    font=(font, 6),
    bg=BG_COLOR,
    fg=TEAL
)

label1.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-40)  # bottom-right corner with small padding
label2.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-20)  
# label3.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)  

restart_program()

# Thread to run number updates without freezing window
running = True
# thread = Thread(target=show_number, daemon=True)
# thread.start()

restart_program()
show_number()
move_banner()


window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()
