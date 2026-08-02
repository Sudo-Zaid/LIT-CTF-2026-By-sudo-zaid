# pathfinder

**Category:** Rev · **Points:** 161 · **Solves:** 86 · **Author:** Ninjaprime

**Flag:** `LITCTF{((())((()))())(((()())))(()(()((((()())))))((()((())((())(()))))(())))}`

## Challenge

> I found this weird little program on an old drive of my grandpa's. It just asks for
> "the thing" and tells you yes or no… Figure out what it's checking, and what it wants
> to hear, so I can finally go find the way.

## Reversing `check`

The binary is stripped/PIE. `main`:

1. Preprocessing loop (`0x1100–0x11cf`) fills a **36×36 table in `.bss`** with a
   Catalan/ballot DP (cumulative sums, 36-qword rows).
2. `fgets` a line, strip `\n`, require prefix `LITCTF{` and suffix `}`.
3. Scan the **inner** string (only `(` and `)`), keeping `A` = opens, `C` = closes,
   and a 64-bit `SUM`:

   ```
   '(' : require A <= 34 ;                          A += 1
   ')' : require A > C   ; SUM += table[A+1][C] ;   C += 1   (table[36..]=0)
   end : require A == 35 && C == 35 && SUM == 0x128e740722b291ad
   ```

So the input must be a **balanced sequence of 35 `(` and 35 `)`** — a Dyck / lattice
path — and `table[a][c]` is `f(a,c)` = the number of ways to complete a valid path from
`(a opens, c closes)` to `(35,35)`:

```
f[a][c] = f[a+1][c]·(a<35) + f[a][c+1]·(a>c),   f[35][35] = 1
f[0][0] = Catalan(35) = 3116285494907301262
```

## Solution — SUM is the path's rank; unrank it

On each `)`, the program adds `f[A+1][C]` = *"how many completions would have chosen
`(` here instead"*. Summed over the path, that's exactly the **lexicographic rank** of
the path (with `(` < `)`). The target:

```
MAGIC = 0x128e740722b291ad = 1337133713371337133      (a leet giveaway)
```

which is `< Catalan(35)`, i.e. a valid rank. **Unrank** it:

```python
R, a, c, path = MAGIC, 0, 0, []
for _ in range(70):
    opens = f[a+1][c] if a < 35 else 0
    if a < 35 and R < opens:  path += '('; a += 1
    else:                     R -= opens; path += ')'; c += 1
assert R == 0 and a == c == 35      # exact -> valid rank
```

`R` lands on exactly `0` with `a == c == 35`, giving the unique path. The flag is
`LITCTF{` + that 70-char parenthesis string + `}`.

## Flag

```
LITCTF{((())((()))())(((()())))(()(()((((()())))))((()((())((())(()))))(())))}
```
