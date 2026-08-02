# sequence lock

**Category:** Rev · **Points:** 156 · **Solves:** 94 · **Author:** Ninjaprime

**Flag:** `LITCTF{f1bon4cci_ch41ns_ftw}`

## Challenge

> An old vault hums with a rhythm only the Fibonacci sequence could love. Feed it the
> right words and it will click open, by jove.

## Reversing `main`

The program reads a candidate flag (`argv[1]` or stdin) and validates it:

1. **Format gate** — `strncmp(input, "LITCTF{", 7) == 0` **and** last char `== '}'`,
   otherwise *"doesn't even recognize that shape of key."*
2. **Length gate** — the inner content (between the braces) is copied out and its length
   must be **exactly `0x14` = 20** (`cmp ebp, 0x14`).
3. **Fibonacci chain** — a running one-byte state (init `0xAA`), for `i = 0..19`:

   ```asm
   ; ecx = fib(i)  (1,1,2,3,5,8,13,21,...  computed inline)
   add  cl, [inner + i]         ; cl = (fib[i] + inner[i]) & 0xff
   xor  r9d, ecx                ; state ^= (fib[i] + inner[i]) & 0xff
   cmp  r9b, [target + i]       ; must equal target[i]
   jne  wrong
   ```

   The 20-byte `target` lives at vaddr `0x2140`:
   `cd ff 9b e9 9a a6 d6 ae 25 b3 0f f7 ea 40 90 de 42 3c f5 11`.

## Solution — invert the chain

Every step is reversible. With `state[-1] = 0xAA`:

```
state[i]                 = target[i]
(fib[i] + inner[i]) & 0xff = state[i] ^ state[i-1] = target[i] ^ target[i-1]
inner[i]                 = ((target[i] ^ prev) - fib[i]) & 0xff
```

```python
fib = [1,1]; 
while len(fib)<20: fib.append(fib[-1]+fib[-2])
prev, inner = 0xAA, []
for i in range(20):
    inner.append(((target[i]^prev) - (fib[i]&0xff)) & 0xff); prev = target[i]
flag = b"LITCTF{" + bytes(inner) + b"}"   # LITCTF{f1bon4cci_ch41ns_ftw}
```

Recovers `f1bon4cci_ch41ns_ftw` — **"fibonacci chains ftw"** — and re-encoding it
reproduces the target exactly.

## Flag

```
LITCTF{f1bon4cci_ch41ns_ftw}
```
