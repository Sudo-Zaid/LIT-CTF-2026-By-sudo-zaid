# faulty image 3

**Category:** Crypto / Stego · **Points:** 256 · **Solves:** 26 · **Author:** Ninjaprime

**Flag:** `LITCTF{p1x3l_p3rf3ct_98xzfq9!}`

## Challenge

> A hacker sent us another suspicious image. We don't know what to do with it. Maybe
> you do? It's pretty colorful though...
>
> **hint:** *What does it being colorful remind you of? Do you see a part of the border
> that is a different color than the rest?*

Provided file: [`corrupt3.png`](corrupt3.png) — a 500×200 image with an orange border, a
dark centre, and a **decoy** flag drawn in red text: `LITCTF{1mAg3_F1ag_1o3fjs!}`.

## Recon

Unlike *faulty image 1*, this PNG is **structurally perfect** — every chunk CRC is
valid (`IHDR` 500×200 RGB8, `IDAT`, `IEND`). So nothing is "broken"; the payload is
hidden **in the pixels**, and the hint points straight at the **border**.

The border is a single solid colour, orange `(255, 157, 0)`. Scanning the **top row**
for anything that isn't that orange turns up exactly **30 anomalous pixels**, evenly
spaced **every 7 px** starting at `x = 7`:

```
x    :  7  14  21  28  35  42  49 ...
color: (76,89,152) (73,86,146) (84,97,168) (67,80,134) (84,97,168) (70,83,140) (123,136,246) ...
```

## Solution — the red channel is the payload

Look at the structure of each anomalous colour `(R, G, B)`:

```
G = R + 13
B = 2 * R
```

The green and blue channels are **derived** from red — they exist only to spread the
value across all three channels so the pixels look "colourful" (that's the hint). The
real data is the **red channel**, and it's plain ASCII:

```
R = 76 73 84 67 84 70 ...  ->  'L' 'I' 'T' 'C' 'T' 'F' ...
```

So just read the R channel of every non-orange pixel in the top row, in order:

```python
from PIL import Image
import numpy as np
a = np.array(Image.open("corrupt3.png").convert("RGB"))
border = (255, 157, 0)
flag = ''.join(chr(int(px[0])) for px in a[0] if tuple(px) != border)
# -> LITCTF{p1x3l_p3rf3ct_98xzfq9!}
```

The 30 red values decode to the real flag. The centered red text
`LITCTF{1mAg3_F1ag_1o3fjs!}` was a decoy the whole time — *pixel perfect*.

## Flag

```
LITCTF{p1x3l_p3rf3ct_98xzfq9!}
```
