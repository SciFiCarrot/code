from pathlib import Path

p = Path("~/dannebrog/animation/frame_1").expanduser()

# If it's a FILE:
text = p.read_text(encoding="utf-8")
print(text)
