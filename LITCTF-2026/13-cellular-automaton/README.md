# cellular automaton

**Category:** Rev · **Points:** 153 · **Solves:** 100 · **Author:** C0DET1GER

**Flag:** `LITCTF{g0ing_b4ck_1n_t1m3}`

## Challenge

> I ran a cellular automaton on my flag and this is the output:
> `652b481a7c203a240b244f045b365f090016050e58227d270b37`
> I forgot what the flag is. Can you get it back?

## Reversing `main`

The 26-byte flag (`0x1a`) is read with `fread`, then:

1. **Expand to bits** — the 26 bytes become 208 cells (bit `i` = `flag[i/8] >> (7-i%8) & 1`,
   MSB-first).
2. **32 generations of Rule 90** on a **cyclic** array of 208 cells:

   ```asm
   left  = cells[(j + 0xcf) % 0xd0]   ; (j-1) mod 208
   right = cells[(j + 1)    % 0xd0]   ; (j+1) mod 208
   new[j] = left XOR right            ; Rule 90
   ```
   outer loop runs `gen = 0..0x1f` → **32** generations, copying `new` back into `cells`
   each time.
3. **Pack** the 208 cells back into 26 bytes and print with `%02x`.

## Solution — it's linear, so invert it

Rule 90 (`new = left ⊕ right`) is **linear over GF(2)**, so 32 generations is a fixed
`208×208` matrix `M` with `output = M · input`. Recover the input by solving the linear
system.

Building `M` (apply the forward transform to each of the 208 unit inputs) and running
Gaussian elimination shows **rank 192** — the map isn't invertible (nullspace dim 16 →
`2^16` valid preimages). To select the real flag, add the known **`LITCTF{`** prefix
(56 bits) as extra equations. That makes the system full rank (208) with a unique,
consistent solution:

```python
# out = M·in over GF(2); solve with LITCTF{ prefix pinned
# -> forward(x) == y verified
flag = b"LITCTF{g0ing_b4ck_1n_t1m3}"
```

*(Rule-90 aside: 32 gens simplifies via Lucas' theorem to
`output[j] = input[(j-32)%208] ⊕ input[(j+32)%208]`, since `C(32,k)` is odd only for
`k∈{0,32}` — but the generic GF(2) solve doesn't need that.)*

The flag — **"going back in time"** — is exactly what we did by undoing the generations.

## Flag

```
LITCTF{g0ing_b4ck_1n_t1m3}
```
