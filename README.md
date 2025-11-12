# Comp-Soc Binary Bingo

This project was developed by **Zoe Weston** for the **University of Surrey Computer Science Society (CompSoc)** as part of *Belonging Week*.  
It provides an interactive, accessible way to host a **Binary Bingo Night**, complete with printable cards, dynamic number displays, and surprise challenge events.

## Overview

The repository includes three key components that work together to create the full Binary Bingo experience:

### **1. Bingo Card Generator**
A Python script that generates unique, printable bingo cards with numbers from **0 to 127**.  
Each card features:
- CompSoc's signature gradient
- A binary card ID for easy verification
- CompSoc logo with styled background
- All output in PDF format for printing

### **2. Binary Number Display**
A **Tkinter-based** GUI application used during the live event.  
It randomly generates binary numbers, displays them in binary form, and then reveals their decimal equivalents.  
Each number is unique, using a **linked list** to ensure no repeats.  
Core features include:
- Displays both binary and decimal forms with user-controlled pacing  
- Includes a scrolling banner of all called numbers  
- Linked list structure ensuring no repeats
- Four-button interface: Start, Next, Reveal, Restart
- Dynamic CompSoc colour gradient for numbers and UI
- Intergrated challenge system triggered at random intervals

### **3. Challenge Database**
A lightweight SQLite database that stores a list of fun challenges and event prompts.
When a challenge occurs during the game, a random entry is fetched and displayed on-screen.

Example entries include:
- “First person to MOOOOOO gets a sweet!”
- “SWITCH CARDS!”
- “Compliment the person next to you!”
This design makes it easy to customise or expand the challenges without editing the main program.

## Features
- Gradient branding: all visuals use CompSoc’s purple–teal palette
- Globally unique cards: every card has verified unique numbers
- Linked list logic: ensures no duplicate numbers are drawn
- Binary + Decimal display: users can control timing manually
- Smooth banner animation: continuously cycles called numbers
- Database-backed challenges: random fun events during play
- Accessibility ready: large, high-contrast visuals and simplified print options

## Requirements

### General
- **Python 3.8+**

### Bingo Card Generator (`bingo_card_generator.py`)
Used to generate printable bingo cards.

**Libraries:**
- Built-in: `random`
- External: `reportlab` – for creating and exporting PDFs; `pillow` – for image and colour gradient handling  

**Install:**
```bash
pip install reportlab pillow
```

### Binary Number Display (`Binary Number Generator.py`)
Used for the GUI which displays all numbers.

**Libaries**
- Built-in: `tkinter`, `random`, `time`, `threading`, `sqlite3`
- Local: `Bingo_Database_Access.py`
No additional installation required beyond standard Python.

### Database Access (Bingo_Database_Access.py)
Used to access the challenges from a separte Database

**Libaries**
- Built-in: `sqlite3`, `random`
- Database file: `Database.db` (inlcuded and editable with any SQLite editor)
No additional installation required.
 
