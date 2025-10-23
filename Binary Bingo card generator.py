from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
import random

# Page setup
W, H = A4
MARGIN = 0.6 * inch
CARD_W = W - 2 * MARGIN
CARD_H = H - 2 * MARGIN

# Color helpers
def hex_to_color(hex_str):
    hex_str = hex_str.strip("#")
    r, g, b = [int(hex_str[i:i+2], 16)/255 for i in (0, 2, 4)]
    return colors.Color(r, g, b)

COLOR_LEFT  = hex_to_color("#ae46ea")   # purple (left)
COLOR_RIGHT = hex_to_color("#28d6a9")   # teal (right)

# Number generator
def generate_card_numbers():
    """Return 25 unique numbers from 0–127 (random order)."""
    return random.sample(range(0,128), 25)

# Gradient background
def draw_gradient_background(c, x, y, w, h, color_left, color_right, steps=50):
    """Lightweight left→right vector gradient."""
    for i in range(steps):
        t = i / (steps - 1)
        r = color_left.red   * (1 - t) + color_right.red   * t
        g = color_left.green * (1 - t) + color_right.green * t
        b = color_left.blue  * (1 - t) + color_right.blue  * t
        c.setFillColor(colors.Color(r, g, b))
        c.rect(x + w * t, y, w / steps + 1, h, stroke=0, fill=1)

# Draw one bingo card
def draw_card(c, x, y, w, h, numbers):
    draw_gradient_background(c, x, y, w, h, COLOR_LEFT, COLOR_RIGHT)

    # Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 46)
    c.drawCentredString(x + w/2, y + h - 1.2*inch, "BINARY BINGO")

    # Grid
    left, right = x + 0.9*inch, x + w - 0.9*inch
    top, bottom = y + h - 2.0*inch, y + 1.0*inch
    col_xs = [left + i*(right-left)/4 for i in range(5)]
    row_ys = [top - j*(top-bottom)/4 for j in range(5)]

    circle_r = min((right-left)/10, (top-bottom)/10)  # size of circles
    c.setFont("Helvetica-Bold", 22)  # numbers font and size

    idx = 0
    for r in range(5):
        for col in range(5):
            cx, cy = col_xs[col], row_ys[r]
            c.setFillColor(colors.white)
            c.setStrokeColor(colors.whitesmoke)
            c.setLineWidth(1.2)
            c.circle(cx, cy, circle_r, stroke=1, fill=1)
            c.setFillColor(colors.black)
            c.drawCentredString(cx, cy - 7, str(numbers[idx]))
            idx += 1

# Build PDF
pdf_path = "Binary_Bingo.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)

seen = set()
for i in range(80):     # number of cards
    while True:
        nums = generate_card_numbers()
        key = tuple(sorted(nums))    # ensure global uniqueness
        numss = tuple(nums)
        if key not in seen:
            seen.add(numss)
            break
    draw_card(c, MARGIN, MARGIN, CARD_W, CARD_H, nums)
    c.showPage()

c.save()
print("Created", pdf_path)
