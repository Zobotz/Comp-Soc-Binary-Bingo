import tkinter as tk
import random
import time
from threading import Thread
from tkinter import PhotoImage

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
reveal_pressed = False
started = False
event_active = False
# banner
called_numbers = []
speed = 3  # pixels per frame for banner scroll
font = ("Arial", 48, "bold")
gap_text = "     "  # gap after the number list in banner
banner_text = ""
banner_height = 80

current_number = None
current_binary= None

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
    global list_size, head, current_number, current_binary
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

    current_number = current.data
    current_binary= format(current_number, "08b")

    # removes chosen number from linked list
    if prev == None:
        head = current.next
    else:
        prev.next = current.next
    list_size -=1

    return current_number, current_binary

def show_binary():
    global next_pressed, started, running
    if not running or not started:
        window.after(100, show_binary)
        return

    if not next_pressed:
        window.after(100, show_binary)
        return
    
    next_pressed = False
    
    # 10% chance of event occuring
    if random.random() < 0.25: # use 0.5 for testing purposes
        trigger_special_event()
        return #----------------------------------------------------------------------------------------
    
    reveal_button.config(state="normal")
    next_button.config(state="disabled")


    # number, binary = random_binary()
    current_number, current_binary = random_binary()
    print(current_number)

    # formats the binary to have 4 bits then a space then the other 4 bits
    def format_binary():
        grouped = [current_binary[i:i+4] for i in range(0, len(current_binary), 4)]
        # Join with a single space between groups
        return (grouped)
    # Show binary first
    label.config(text=format_binary(), fg=PURPLE)

def reveal_number():
    global current_number, reveal_pressed, started, running
    if not running or not started or current_number is None:
        return

    reveal_pressed = False
    factor = current_number / 127
    colour = choose_colour(TEAL, PURPLE, factor)

    label.config(text=str(current_number), fg=colour)
    called_numbers.insert(0, current_number)
    update_banner_text()
    window.after(100, show_binary)

    reveal_button.config(state="disabled")
    next_button.config(state="normal")

# buttons functions
def start_program():
    global started
    started = True
    start_button.config(state="disabled")
    next_button.config(state="normal")
    reveal_button.config(state="disabled")

def next_number():
    global next_pressed, event_active
    if event_active:
        # leave a clean slate, restore font, and immediately resume
        label.config(text="", fg=PURPLE, font=(font, 200, "bold"))
        event_active = False
        next_pressed = True
        window.after(0, show_binary)   # <- IMPORTANT: resume now
        return
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
    start_button.config(state="normal")
    next_button.config(state="disabled")
    reveal_button.config(state="disabled")

# set up the linked list before starting
head = setInitalList()
current=head

# create window
window = tk.Tk()
window.title("Binary Display with Bingo Banner")
window.geometry("800x350") # increased height for banner + main display
window.configure(bg=BG_COLOR)

# --- Logo (plain Tkinter, no PIL) ---
try:
    logo_img = tk.PhotoImage(file="vectorWithFancyEdges.png")  # file in same folder
    logo_img = logo_img.subsample(6, 6)

except Exception as e:
    print("Failed to load logo:", e)
    logo_img = None

if logo_img:
    # Optional: downscale if too big (integer factors only)
    # e.g., halves size -> subsample(2, 2). Adjust as needed.
    # logo_img = logo_img.subsample(2, 2)

    logo_label = tk.Label(window, image=logo_img, bg=BG_COLOR, borderwidth=0)
    logo_label.image = logo_img  # keep a reference!
    # Center on the window
    logo_label.place(x=15, y=90, anchor="nw")
    logo_label.lift()  # bring above everything

    # If other widgets keep covering it, nudge it to the top periodically:
    def keep_logo_on_top():
        logo_label.lift()
        window.after(1000, keep_logo_on_top)

    keep_logo_on_top()


# Banner Canvas
banner_canvas = tk.Canvas(window, width=800, height=banner_height, bg="black", highlightthickness=0)
banner_canvas.pack(side="top", fill="x")
banner_canvas.update()

# Track banner text items
text_items = []
text_width = 0

def update_banner_text():
    global text_items, text_width
    banner_canvas.delete("all")  # clear the canvas
    text_items = []

    y = banner_height // 2
    x = 1500  # start position off-screen right

    if not called_numbers:
        # Default message before game starts
        item = banner_canvas.create_text(
            x, y,
            text="Waiting for numbers...",
            font=font,
            fill=TEAL,
            anchor="w"
        )
        text_items.append(item)
        banner_canvas.update()
        bbox = banner_canvas.bbox(item)
        text_width = bbox[2] - bbox[0]
        return

    # Draw all numbers with gradient colors
    for num in (called_numbers):  # newest numbers appear last
        factor = num / 127
        color = choose_colour(TEAL, PURPLE, factor)

        item = banner_canvas.create_text(
            x, y,
            text=str(num),
            font=font,
            fill=color,
            anchor="w"
        )
        text_items.append(item)

        bbox = banner_canvas.bbox(item)
        width = bbox[2] - bbox[0] + 40  # add space between numbers
        x += width

    banner_canvas.update()
    bbox = banner_canvas.bbox("all")
    text_width = bbox[2] - bbox[0]

def move_banner():
    global text_width
    for item in text_items:
        banner_canvas.move(item, -speed, 0)

    # Check if everything has scrolled off the left edge
    if text_items:
        x = banner_canvas.coords(text_items[-1])[0]
        if x + text_width < 5:
            update_banner_text()

    window.after(20, move_banner)

def reset_banner_position():
    # Reset everything back to starting position on restart
    update_banner_text()

# special event for something random to happen
def trigger_special_event():
    global event_active
    event_active = True

    label.config(text="CHALLENGE TIME!", fg="#ff3333", font=("Helvetica", 100, "bold"))
    next_button.config(state="normal")     # user can press Next to exit event
    reveal_button.config(state="disabled")



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

next_button = tk.Button(button_frame, text="Next", command=next_number, font=(font, 16), bg = '#7A7ED9')
next_button.grid(row=0, column=1, padx=10)

reveal_button = tk.Button(button_frame, text="Reveal", command=reveal_number, font=(font, 16), bg = '#5C9EBC')
reveal_button.grid(row=0, column=2, padx=10)

restart_button = tk.Button(button_frame, text="Restart", command=restart_program, font=(font, 16), bg=TEAL)
restart_button.grid(row=0, column=3, padx=10)

# credit label (placed bottom-right)
label1 = tk.Label(
    window,
    text="Code by Zoe Weston",
    font=(font, 16, "bold"),
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
# thread = Thread(target=show_binary, daemon=True)
# thread.start()

restart_program()
show_binary()
move_banner()


window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()