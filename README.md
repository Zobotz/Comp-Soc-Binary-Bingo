# Comp-Soc Binary Bingo

This project was developed by **Zoe Weston** for the **University of Surrey Computer Science Society (CompSoc)** as part of *Belonging Week*.  
It provides interactive tools for hosting a **Binary Bingo Night**, complete with printable cards and a dynamic number display.

## Overview

The repository includes two main components:

### **Bingo Card Generator**
A Python script that generates unique, printable bingo cards with numbers from **0 to 127**.  
Each card features CompSoc’s signature gradient colours (`#ae46ea → #28d6a9`) and exports as a **PDF** for easy printing.

### **Binary Number Display**
A **Tkinter-based** graphical application used during the bingo game.  
It randomly generates binary numbers, displays them in binary form, and then reveals their decimal equivalents.  
Each number is unique, using a **linked list** to ensure no repeats.  

Recent versions now include:
- Smooth **scrolling banner** showing all called numbers  
- Dynamic **gradient colours** that match the CompSoc theme  
- Configurable **restart** and **timing behaviour**  
- Buttons for **Next**, **Reveal**, **Restart**, and **Start**  
- Ready for expansion with **random challenge events**  

## Features

- Generates globally unique bingo cards (no duplicates)  
- Uses CompSoc’s brand colours in a smooth gradient  
- Displays both binary and decimal forms interactively  
- Includes a scrolling banner of called numbers  
- Adjustable scroll speed and restart timing  
- Output in print-ready PDF format for easy distribution  
- Simple, modern graphical interface using Tkinter  

## Requirements

### General
- **Python 3.8+**

### Bingo Card Generator (`bingo_card_generator.py`)
Used to generate printable bingo cards.

**Libraries:**
- `reportlab` – for creating and exporting PDFs  
- `pillow` – for image and colour gradient handling  

**Install:**
```bash
pip install reportlab pillow
