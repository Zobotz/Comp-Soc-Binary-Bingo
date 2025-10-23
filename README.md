# Comp-Soc-Binary-Bingo
This project was developed by the University of Surrey Computer Science Society as part of Belonging Week. It provides tools to generate and display binary bingo cards for use in a society bingo night.

## Overview
The repository includes:
**Bingo Card Generator** – A Python script that creates unique, printable bingo cards using numbers from 0 to 127. Each card features the CompSoc gradient colours (#ae46ea → #28d6a9) and is saved to a PDF file for easy printing.
**Binary Number Display** – A Tkinter-based application that generates a random number between 0 and 127, displays its binary form for a few seconds, then reveals the decimal equivalent. The program uses a linked list to ensure that no number is repeated.

## Features:
Generates globally unique bingo cards (no duplicates)
Uses CompSoc brand colours in a smooth gradient
Simple graphical interface for the binary number display
Adjustable timings and design options
Output in PDF format for print-ready cards

## Requirements:
### General
Python 3.8+

### Bingo Card Generator (bingo_card_generator.py):
Used to generate unique printable bingo cards in PDF format.
**Libraries:**
reportlab – for creating and exporting the PDF files
pillow – for image and colour handling (used for gradients and backgrounds)
**Install:**
pip install reportlab pillow

### Binary Number Display (binary_display.py)
A graphical display that shows random binary and decimal numbers.
All required modules are included with Python.
**Built-in modules:**
tkinter
random
time
threading
No additional installation is required.
