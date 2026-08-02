# Any Secrets Could Instantly Imparted

**Category:** Crypto · **Points:** 207 · **Solves:** 44 · **Author:** joshadoodle

**Flag:** `LITCTF{ASCII-jUl1us-c43s4r-gewowa}`

## Challenge

> Cody and Tiger have just had an argument, where Cody has shared Tiger's deepest,
> darkest secret. The following was one of their recorded interactions during their argument.
>
> **Tiger:** Et tu, Brute?
> **Cody:** `HEP?PBw=O?EE)fQh-qo)_0/o0n)casks]y.`
>
> Note that the flag will be in the format `LITCTF{...}`.

## Recon — reading the hints

The challenge hands you two clues, one in the title and one in Tiger's line.

1. **Title acrostic** — *"**A**ny **S**ecrets **C**ould **I**nstantly **I**mparted"* →
   the first letters spell **`ASCII`**.
2. **"Et tu, Brute?"** — Julius Caesar's dying words → **Caesar cipher**. The word
   *"Brute"* doubles as a nudge toward **brute forcing** the shift.

Put together: it's a **Caesar shift, but over raw ASCII byte values** rather than only
the 26 letters. That's why the ciphertext is full of symbols and digits
(`?`, `=`, `)`, `-`, `/`, `0`, `]`, …) — every printable byte is shifted, not just `A–Z`.

## Solution

We know the plaintext must begin with `LITCTF{`. Line that up against the ciphertext:

| plain | `L` | `I` | `T` | `C` | `T` | `F` | `{` |
|-------|----|----|----|----|----|----|----|
| ascii | 76 | 73 | 84 | 67 | 84 | 70 | 123 |
| cipher| `H` | `E` | `P` | `?` | `P` | `B` | `w` |
| ascii | 72 | 69 | 80 | 63 | 80 | 66 | 119 |

Every column differs by exactly **4** (`cipher = plain − 4`), so recovering the plaintext
is just `plain = cipher + 4` on each byte. No need to guess — brute forcing all 255 shifts
and keeping the one that produces `LITCTF{…}` lands on the same answer.

```python
CIPHER = "HEP?PBw=O?EE)fQh-qo)_0/o0n)casks]y"   # trailing '.' is sentence punctuation
for shift in range(1, 256):
    dec = ''.join(chr((ord(c) + shift) % 256) for c in CIPHER)
    if dec.startswith("LITCTF{") and dec.endswith("}"):
        print(shift, dec)      # -> 4  LITCTF{ASCII-jUl1us-c43s4r-gewowa}
```

The decoded flag reads **`ASCII-jUl1us-c43s4r`** = "ASCII Julius Caesar", confirming the
mechanism.

> **Note on the trailing `.`** — Cody's message ends with a period. That `.` is just the
> punctuation of the sentence: decoding it gives `2`, which would land *after* the closing
> `}`. So it isn't part of the ciphertext, and the flag ends at the brace.

## Flag

```
LITCTF{ASCII-jUl1us-c43s4r-gewowa}
```
