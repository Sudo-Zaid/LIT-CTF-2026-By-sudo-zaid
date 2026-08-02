# extremely original

**Category:** crypto · **Points:** 376 · **Solves:** 8 · **Author:** joshadoodle

> It seems that I have accidentally leaked my flag: `oyO+UrMXccyqeo2W+WA5jZPVXNSAyYVwGt`
>
> Good thing that my computer generated keys before releasing the flag to the public.
> The flag for this challenge will be "LITCTF" followed by a string of characters.
> Make sure to insert curly braces: `LITCTF{...}`.

No attachment — the 34-character string *is* the whole challenge.

**Flag:** `LITCTF{tH3+XOR+fuNct10n+1s/n0t+s4F3}`

---

## 1. Reading the hints

| Hint | Meaning |
|---|---|
| **"e*X*tremely *OR*iginal"** | the combiner is **XOR** |
| "my computer generated **keys**" | the keystream comes from a **PRNG**, not from a passphrase |
| "Make sure to **insert curly braces**" | the plaintext contains **no braces** — the alphabet cannot represent them |

## 2. The leak is *not* base64 of a byte string

The obvious first move is `base64.b64decode(s + '==')` → 25 bytes. That is a trap:

```
34 chars x 6 bits = 204 bits;  25 bytes = 200 bits
```

so the **last symbol carries 4 padding bits that must be zero** in real base64. For 25
bytes the final character can only be one of `A Q g w` (index ≡ 0 mod 16). Ours is `t`
(index 45 = `0b101101`) — the pad bits are `1101`:

```python
ALPH.index('t') & 15   # -> 13, must be 0 for valid b64 of 25 bytes
```

Therefore the string is **not** an encoded byte blob. It is **34 independent base64
symbols — one per plaintext character**, and the cipher works on the 6-bit alphabet
*indices*:

```
c_i = p_i XOR k_i          (all values in 0..63)
```

That also explains the curly-brace note: `{` and `}` (and `_`) simply do not exist in
the 64-character alphabet, so the author had to hand the braces back to the player.
Plaintext length 34 = `LITCTF` + 28 characters of body.

## 3. Recovering the keystream

Six characters of known plaintext give six keystream symbols for free:

```python
ALPH = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
ks = [ALPH.index(c) ^ ALPH.index(p) for c, p in zip('oyO+Ur', 'LITCTF')]
# [35, 58, 29, 60, 7, 46]
```

"My **computer generated** keys" is the tell: a lazy, textbook generator. Trying the
smallest possible one — a **linear congruential generator working directly modulo 64** —
the entire parameter space is only `64 x 64 x 64 = 262144` triples `(a, c, k0)`, brute
forced in well under a second against the `LITCTF` prefix:

```python
k_{i+1} = (21 * k_i + 27) mod 64,     k_0 = 35
```

Check: `21*35+27 = 762 ≡ 58`, `21*58+27 = 1245 ≡ 29`, `21*60+27 = 1287 ≡ 7` … it
reproduces the leaked prefix keystream exactly, and (`a-1` divisible by 4, `c` odd) the
generator has full period 64 > 34, so no symbol repeats.

## 4. Decryption

```python
s, ks = 35, []
for _ in range(34):
    ks.append(s); s = (21*s + 27) % 64
pt = ''.join(ALPH[ALPH.index(c) ^ k] for c, k in zip(CT, ks))
# LITCTFtH3+XOR+fuNct10n+1s/n0t+s4F3
```

Re-encrypting the recovered plaintext reproduces the leak byte-for-byte, and the body
reads as English — `+` and `/` are the only word separators the base64 alphabet offers:

```
tH3 + XOR + fuNct10n + 1s / n0t + s4F3     ->  "the XOR function is not safe"
```

```
LITCTF{tH3+XOR+fuNct10n+1s/n0t+s4F3}
```

## 5. Takeaways

* **Check the padding bits.** A base64-looking string whose length is not a multiple of
  4 *and* whose trailing bits are non-zero is not encoded bytes — it is a stream of
  6-bit symbols. Chasing the 25-byte decode sends you brute-forcing PRNG seeds forever
  (Mersenne Twister over `int(time.time())`, MSVC `rand()`, …) against a target that was
  never there.
* **A missing `{`/`}` in a flag is an alphabet fingerprint.** When the author asks you to
  re-insert the braces, the cipher alphabet is telling you its size — here, 64.
* **Try the tiny keyspaces first.** Before brute-forcing 2^32 PRNG seeds, test whether
  the keystream is affine (`k_i = a*i+b`) or a small-modulus LCG. Both spaces are under
  2^18 and cost milliseconds.

## Files

* [`solve.py`](solve.py) — brute-forces the LCG triple from the `LITCTF` crib and prints the flag.
