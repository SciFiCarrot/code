import sys
import time
from pathlib import Path

# Hide cursor (we'll show it again at the end)
HIDE = "\x1b[?25l"
SHOW = "\x1b[?25h"
CLEAR = "\x1b[2J"
HOME = "\x1b[H"


p1 = Path("~/dannebrog/animation/frame_1").expanduser()
p2 = Path("~/dannebrog/animation/frame_2").expanduser()
p3 = Path("~/dannebrog/animation/frame_3").expanduser()
p4 = Path("~/dannebrog/animation/frame_4").expanduser()

# If it's a FILE:
text1 = p1.read_text(encoding="utf-8")
text2 = p2.read_text(encoding="utf-8")
text3 = p3.read_text(encoding="utf-8")
text4 = p4.read_text(encoding="utf-8")


frames = []

frames.append(text1)
frames.append(text2)
frames.append(text3)
frames.append(text4)

print(frames)


def animate(frames, fps=5, loops=100):
    try:
        sys.stdout.write(HIDE)
        for _ in range(loops):
            for f in frames:
                sys.stdout.write(CLEAR + HOME + f)
                sys.stdout.flush()
                time.sleep(1.0 / fps)
    finally:
        sys.stdout.write(SHOW)
        sys.stdout.flush()


if __name__ == "__main__":
    animate(frames)
