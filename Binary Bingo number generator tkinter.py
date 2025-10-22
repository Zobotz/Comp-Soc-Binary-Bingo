import tkinter as tk
import random
import time
from threading import Thread

# Colours
PURPLE = "#ae46ea"
TEAL = "#28d6a9"
BG_COLOR = "#1a1a1a"

# Random binary generator
def random_binary():
    number = random.randint(0, 127)
    binary = format(number, "08b")
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
