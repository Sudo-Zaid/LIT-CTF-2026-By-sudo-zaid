# space radiation

**Category:** misc · **Points:** 162 · **Solves:** 84 · **Author:** joshadoodle

> We've received this transmission from space. However, it seems that some radiation
> has altered the message! Help us recover the original, important message:
>
> `84ea cc57 4906 d24c cebd 93a2 3508 b04d 8b8f 8731 bc5a 0675 8a39 4143 b443 9ec3 030b b014 7066 5c34 2c18 b151 cb44 823d`

**Flag:** `LITCTF{h4MM1nG-3Rr0r_C0rR3cT10N!}`

---

## Recon

The prompt is pure theme-telegraphing:

- **"space radiation ... altered the message"** → *Single Event Upsets* — high-energy
  particles flipping individual bits in memory. The classic real-world defence is
  **ECC memory using Hamming SECDED codes**.
- **"recover the original message"** → the data is redundant enough to *correct* the
  flips, not just detect them.

Count the data: **24 groups of 2 bytes = 24 × 16-bit words**.

A 16-bit word is the textbook size for an **extended Hamming(16,11)** codeword:

| bits | role |
|:----:|------|
| 4 | Hamming parity (positions 1, 2, 4, 8) |
| 1 | overall parity (position 0) → SECDED |
| **11** | **data** |

So each word carries 11 real bits: `24 × 11 = 264 bits = 33 bytes` — exactly the length
of a `LITCTF{...}` flag with a 25-char body. That alignment confirms the encoding before
writing a line of code.

## The code (extended Hamming / SECDED)

Number the 16 bit-positions `0..15`, **MSB-first** (position 0 = MSB, position 15 = LSB):

- Positions that are powers of two — **1, 2, 4, 8** — are Hamming **parity** bits.
- Position **0** is the **overall parity** bit (this is what upgrades plain SEC to
  **SEC-DED**: Single Error Correct, Double Error Detect).
- The remaining eleven positions — **3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15** — are the
  **data** bits.

### Correcting one flip per word

For each codeword, XOR together every position index (1..15) that currently holds a `1`.
That value is the **syndrome**:

- syndrome `= 0` → the word is clean.
- syndrome `= s ≠ 0` → the bit at **position `s`** was flipped by radiation; flip it back.

That's the whole trick — the syndrome *is* the address of the broken bit. After correcting,
read the 11 data positions out in order, concatenate across all 24 words, and pack the
264 bits MSB-first into 33 bytes.

```python
DATA_POS = [p for p in range(1, 16) if p & (p - 1)]   # 3,5,6,7,9,10,11,12,13,14,15

def decode_word(word):
    b = [(word >> (15 - i)) & 1 for i in range(16)]   # MSB-first positions
    syndrome = 0
    for i in range(1, 16):
        if b[i]:
            syndrome ^= i
    if syndrome:                 # single-bit error -> the syndrome names the bit
        b[syndrome] ^= 1
    return [b[p] for p in DATA_POS]
```

## Result

Running [`solve.py`](solve.py):

```
[+] corrected 20/24 radiation-flipped words
[+] 33 bytes recovered
[+] FLAG: LITCTF{h4MM1nG-3Rr0r_C0rR3cT10N!}
```

**20 of the 24 words** carried a flipped bit — the syndrome pointed straight at each one,
and every correction landed a clean ASCII byte. The flag literally names the technique:

```
LITCTF{h4MM1nG-3Rr0r_C0rR3cT10N!}
```

## Gotchas

- **Convention matters.** The bit-order (MSB-first vs LSB-first) and the bit-packing order
  must both be MSB-first here. The wrong combination corrects the *wrong* position and
  yields garbage — worth brute-forcing the four combinations if the first read isn't ASCII.
- **Don't skip the correction.** Naively pulling the 11 data bits without applying the
  syndrome gives scrambled text, because 20/24 words are actually corrupted.
- The overall-parity bit (position 0) isn't needed to *correct* here (every word has at
  most one flip), but it's what makes this genuinely SECDED rather than plain Hamming.
