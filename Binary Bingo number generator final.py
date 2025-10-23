
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

    # wait for Next button press
    if not next_pressed:
      time.sleep(0.1)
      continue

    next_pressed = False

    # Generate random number
    number, binary = random_binary()

    # prints to console for checking at end
    print(number)

    # Show binary
    label.config(text=binary, fg=PURPLE)
    window.update()
    time.sleep(5)

    # Show decimal
    label.config(text=str(number), fg=TEAL)
    window.update()
    # time.sleep(5) # changed to have next button

def start_program():
    global started
    started = True
    start_button.config(state="disabled")  # disable start after pressing


def next_number():
    global next_pressed
    next_pressed = True


def restart_program():
    global started
    setInitalList()
    started = False
    label.config(text="Press Start", fg=PURPLE)
    start_button.config(state="normal")


head = setInitalList()
current=head

# Create window
window = tk.Tk()
window.title("Binary Display")
window.geometry("800x300") # window size
window.configure(bg=BG_COLOR)

# Big text label
label = tk.Label(
    window,
    text="",
    font=("Helvetica", 80, "bold"), # font and size of text
    bg=BG_COLOR,
    fg=PURPLE
)
label.pack(expand=True)

# Buttons
button_frame = tk.Frame(window, bg=BG_COLOR)
button_frame.pack(pady=20)

start_button = tk.Button(button_frame, text="Start", command=start_program, font=("Helvetica", 16), bg=PURPLE)
start_button.grid(row=0, column=0, padx=10)

next_button = tk.Button(button_frame, text="Next", command=next_number, font=("Helvetica", 16), bg = '#6b8eca')
next_button.grid(row=0, column=1, padx=10)

restart_button = tk.Button(button_frame, text="Restart", command=restart_program, font=("Helvetica", 16), bg=TEAL)
restart_button.grid(row=0, column=2, padx=10)

restart_program()

# Thread to run updates without freezing window
running = True
thread = Thread(target=show_number, daemon=True)
thread.start()

# Close safely on exit
def on_close():
    global running
    running = False
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()
