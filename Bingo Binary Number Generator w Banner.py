import tkinter as tk
import random
import time
from threading import Thread

# Global variables  
# Colours
PURPLE = "#ae46ea"
TEAL = "#28d6a9"
BG_COLOR = "#1a1a1a"

list_size = 0
head = None
next_pressed = False
started = False

# Setting up linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def setInitalList():
    global head, list_size
    list_size = 0
    head = None
    last = None
    for x in range(128):
        newNode = Node(x)
        if head == None:
            head = newNode
        else:
            last.next = newNode
        last=newNode
        list_size+=1
    return head

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
    global running, next_pressed, started
    while running:
        if not started:
            time.sleep(0.1)
            continue

        if not next_pressed:
            time.sleep(0.1)
            continue

        next_pressed = False

        number, binary = random_binary()

        # prints to console for checking at end
        print(number)

        # Show binary
        label.config(text=binary, fg=PURPLE)
        window.update()
        time.sleep(3)

        # Show decimal
        label.config(text=str(number), fg=TEAL)
        window.update()

        # Now update banner AFTER the decimal number is shown
        called_numbers.insert(0, number)
        update_banner_text()

        # no more delay here; waiting for next button press


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

head = setInitalList()
current=head

# --- Banner Globals ---
called_numbers = []
speed = 3  # pixels per frame for banner scroll
font = ("Arial", 48, "bold")
gap_text = "     "  # gap after the number list in banner
banner_text = ""
banner_height = 80

# --- Create window ---
window = tk.Tk()
window.title("Binary Display with Bingo Banner")
window.geometry("800x350") # increased height for banner + main display
window.configure(bg=BG_COLOR)

# --- Banner Canvas ---
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

# --- Banner scroll logic ---
def move_banner():
    global text_width
    banner_canvas.move(text_item, -speed, 0)
    x = banner_canvas.coords(text_item)[0]

    if x + text_width < 0:
        # Reset position to start from right again
        banner_canvas.coords(text_item, 1500, banner_height // 2)


    window.after(20, move_banner)

def update_banner_text():
    global text_width
    if called_numbers:
        text = "  ".join(map(str, called_numbers)) + gap_text
    else:
        text = "Waiting for numbers..." + gap_text

    banner_canvas.itemconfig(text_item, text=text)
    banner_canvas.update()  # Important!

    bbox = banner_canvas.bbox(text_item)
    text_width = bbox[2] - bbox[0]

    canvas_width = banner_canvas.winfo_width()
    banner_canvas.coords(text_item, 1500, banner_height // 2)




def reset_banner_position():
    # Reset banner to start at right edge
    banner_canvas.coords(text_item, 800, banner_height//2)

# --- Big text label for binary/decimal ---
label = tk.Label(
    window,
    text="",
    font=("Helvetica", 200, "bold"), # font and size of text
    bg=BG_COLOR,
    fg=PURPLE
)
label.pack(expand=True)

# --- Buttons ---
button_frame = tk.Frame(window, bg=BG_COLOR)
button_frame.pack(pady=20)

start_button = tk.Button(button_frame, text="Start", command=start_program, font=("Helvetica", 16), bg=PURPLE)
start_button.grid(row=0, column=0, padx=10)

next_button = tk.Button(button_frame, text="Next", command=next_number, font=("Helvetica", 16), bg = '#6b8eca')
next_button.grid(row=0, column=1, padx=10)

restart_button = tk.Button(button_frame, text="Restart", command=restart_program, font=("Helvetica", 16), bg=TEAL)
restart_button.grid(row=0, column=2, padx=10)

# credit label (placed bottom-right)
label1 = tk.Label(
    window,
    text="Code by Zoe Weston",
    font=("Helvetica", 10, "bold"),
    bg=BG_COLOR,
    fg=TEAL
)
label2 = tk.Label(window,
    text="And Isabelle Wickens",
    font=("Helvetica", 6),
    bg=BG_COLOR,
    fg=TEAL
)
label3 = tk.Label(window,
    text="And Chatgpt",
    font=("Helvetica", 1),
    bg=BG_COLOR,
    fg=TEAL
)

label1.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-40)  # bottom-right corner with small padding
label2.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-20)  # bottom-right corner with small padding
label3.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)  # bottom-right corner with small padding

restart_program()

# --- Thread to run number updates without freezing window ---
running = True
thread = Thread(target=show_number, daemon=True)
thread.start()

# --- Start banner scrolling ---
move_banner()

# --- Close safely on exit ---
def on_close():
    global running
    running = False
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()
