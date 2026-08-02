# faulty image 4

**Category:** Crypto / Stego · **Author:** Ninjaprime

**Flag:** `LITCTF{pr1m3_n1bbl3s_77zq!}`

## Challenge

> Something's off about this image. The flag you see isn't the flag you want... again.
> This time, the hacker corrupted some of the pixels, separating them from encoding
> information together as a whole.
>
> **hint:** *Some pixels have unusually small blue values, almost like they've been
> clipped to 4 bits. Which pixels exactly?*

Provided file: [`corrupt4.png`](corrupt4.png) — 500×200, renders a decoy flag.

## Recon

The hint says to find pixels whose **blue channel is clipped to 4 bits** — i.e.
`blue < 16`. Masking those out of the image gives **54 pixels, all in row 0**:

```python
B = a[:, :, 2]
ys, xs = np.where(B < 16)      # ys are all 0
```

The interesting part is *where* they are. The x-coordinates are:

```
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, ... , 241, 251
```

Every one is **prime**. That's the "*which pixels exactly?*" — the marked pixels sit at
**prime x-positions** along the top row. (The rest of the row's blue values are large/
normal, which is what "separates" these from the surrounding pixels.)

## Solution — prime nibbles

Each clipped blue value is a **4-bit nibble** (`0–15`). Read the nibbles left-to-right
(prime order) and pack **two per byte, high-nibble first**:

```python
nib  = [int(B[0, x]) for x in sorted(xs)]                    # 54 nibbles
flag = bytes((nib[i] << 4) | nib[i+1] for i in range(0, len(nib)-1, 2))
# -> b'LITCTF{pr1m3_n1bbl3s_77zq!}'
```

54 nibbles → 27 bytes → the flag. The theme is literally spelled out: **prime nibbles**.

## Flag

```
LITCTF{pr1m3_n1bbl3s_77zq!}
```
