#!/usr/bin/env python3
import math
import sys
import time

ESC = "\x1b"
CLEAR = ESC + "[2J"
HOME = ESC + "[H"
HIDE = ESC + "[?25l"
SHOW = ESC + "[?25h"
RESET = ESC + "[0m"

# --- Flag parameters (Dannebrog-ish proportions) ---
H = 16  # flag height in text cells (not pixels)
W = 48  # flag width in text cells
VERT_STRIPE_X = 10  # column index of the vertical white stripe
HORZ_STRIPE_Y = 7  # row index of the horizontal white stripe
STRIPE_THICK = 2  # thickness (rows/cols) of stripes

# Use background colors to “paint” the flag
RED_BG = ESC + "[41m"
WHITE_BG = ESC + "[47m"

# To make cells look more square in terminal, render each cell as two spaces
CELL = "  "

# Precompute a base flag (no wind)
base = [[RED_BG for _ in range(W)] for _ in range(H)]
for y in range(H):
    for x in range(W):
        if (abs(x - VERT_STRIPE_X) < STRIPE_THICK) or (
            abs(y - HORZ_STRIPE_Y) < STRIPE_THICK
        ):
            base[y][x] = WHITE_BG


def render_frame(phase, amp=3.0, wavelength=10.0):
    """
    phase: advancing angle in radians
    amp:   max horizontal shift in columns
    wavelength: rows per full 2π cycle (bigger = gentler wave)
    """
    out_lines = []
    for y in range(H):
        shift = int(round(amp * math.sin((2 * math.pi / wavelength) * y + phase)))
        # sample base row with wrapping shift to create the wave
        row = base[y]
        shifted = row[-shift % W :] + row[: -shift % W] if shift else row
        # compress repeating background codes by grouping same-color cells
        # (optional micro-optimization for flickerless output)
        line = []
        cur_color = None
        count = 0
        for color in shifted:
            if color != cur_color:
                if cur_color is not None:
                    line.append(cur_color + CELL * count)
                cur_color = color
                count = 1
            else:
                count += 1
        if cur_color is not None:
            line.append(cur_color + CELL * count)
        out_lines.append("".join(line) + RESET)
    return "\n".join(out_lines)


def main():
    fps = 30
    phase = 0.0
    speed = 2.2 / fps  # radians per frame
    try:
        sys.stdout.write(HIDE)
        while True:
            sys.stdout.write(CLEAR + HOME)
            sys.stdout.write(render_frame(phase))
            sys.stdout.flush()
            phase += speed
            time.sleep(1.0 / fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(RESET + SHOW)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
