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

# class for the linked list nodes
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
  
  #randomly chooses the linked list position
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
    while running:
        # Generate random number
        number, binary = random_binary()
        
        # Show binary
        label.config(text=binary, fg=PURPLE)
        window.update()
        time.sleep(10)  # wait 10 seconds

        # Show decimal
        label.config(text=str(number), fg=TEAL)
        window.update()
        input("") # waits for user input before going to next number

head = setInitalList()
current=head

# Create window
window = tk.Tk()
window.title("Binary Display")
window.geometry("600x300")
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
