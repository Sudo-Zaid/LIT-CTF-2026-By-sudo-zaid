#!/usr/bin/env python3
"""
LIT CTF 2026 — crypto/stego — "faulty image 3"

The PNG (500x200, RGB) is structurally perfect (all chunk CRCs valid) and visibly
renders a DECOY flag: LITCTF{1mAg3_F1ag_1o3fjs!}.

Hint: "What does it being colorful remind you of? Do you see a part of the border that
is a different color than the rest?"

The border is a solid orange (255,157,0). Along the TOP row, 30 pixels — one every
7px starting at x=7 — are a different (blue-ish) color. Each is (R, R+13, 2R): the
green/blue channels are just there to make it look "colorful", while the RED channel
carries an ASCII byte. Read the R channel of those pixels in order -> real flag.
"""
from PIL import Image
import numpy as np, os

SRC = os.path.join(os.path.dirname(__file__), "corrupt3.png")

def main():
    a = np.array(Image.open(SRC).convert("RGB"))
    top = a[0]
    border = (255, 157, 0)
    flag = ''.join(chr(int(px[0])) for px in top if tuple(px) != border)
    print("[+] flag:", flag)

if __name__ == "__main__":
    main()
