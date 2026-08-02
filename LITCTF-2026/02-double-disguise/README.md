# Double Disguise

**Category:** Crypto · **Points:** 197 · **Solves:** 50 · **Author:** modulus998244353

**Flag:** `LITCTF{F1fa_W0rld_cup}`

## Challenge

> Oopps, I ran accidentally ran an encryption program on my flag. Now I only have:
> `ZmN+aX5sUWwbTEt1fRpYRk51SV9aVw==`
>
> Can you help me the original flag?

## Recon

The title **"Double Disguise"** says there are **two** layers of obfuscation stacked
on the flag.

- The ciphertext ends in `==` and uses only the base64 alphabet → **layer 1 is Base64**.
- Base64-decoding gives non-printable garbage (`fc~i~lQl\x1bLKu}…`), so there's a
  **second layer** on top.

## Solution

Decode the outer Base64, then figure out layer 2 using the known flag prefix `LITCTF{`.

XOR the decoded bytes against `LITCTF{` position-by-position:

| decoded | 102 | 99 | 126 | 105 | 126 | 108 | 81 |
|---------|----|----|-----|-----|-----|-----|----|
| `LITCTF{`| 76 | 73 | 84  | 67  | 84  | 70  | 123|
| **XOR** | 42 | 42 | 42  | 42  | 42  | 42  | 42 |

Every position returns **42 (`0x2A`)** → layer 2 is a **single-byte XOR** with key `0x2A`.
Applying it to the full buffer recovers the flag.

```python
import base64
raw  = base64.b64decode("ZmN+aX5sUWwbTEt1fRpYRk51SV9aVw==")
key  = raw[0] ^ ord("L")                       # 0x2A
flag = bytes(b ^ key for b in raw).decode()    # LITCTF{F1fa_W0rld_cup}
```

So the "encryption program" was just **XOR(0x2A) then Base64** — trivially reversible
once the prefix leaks the key.

## Flag

```
LITCTF{F1fa_W0rld_cup}
```
