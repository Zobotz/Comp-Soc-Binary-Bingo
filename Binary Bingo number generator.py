import random, time
from IPython.display import clear_output

for i in range(5):  # show 5 random numbers
    number = random.randint(0, 127)
    binary = format(number, '08b')
    clear_output(wait=True)
    print(f"Binary: {binary}")
    time.sleep(5)
    print(f"Decimal: {number}")
    input("")