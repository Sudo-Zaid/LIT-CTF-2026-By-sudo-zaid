# pw.zip

**Category:** Misc · **Points:** 141 · **Solves:** 132 · **Author:** halp

**Flag:** `LITCTF{password_123456_103flkj3}`  ·  **Password:** `1234qwer`

## Challenge

> Thought this password-protected zip would keep the flag safe, but I just found out the
> password I used was one of the 100 most used passwords of 2025!

## Solution

The zip holds a single encrypted `flag.txt`. Checking the headers shows it's **WinZip
AES-256**, not legacy ZipCrypto:

```
compress_type = 99            # AES
extra = ...4145 03 0000       # 'AE' v?, strength 03 = AES-256
```

Python's stdlib `zipfile` throws `NotImplementedError: That compression method is not
supported` on AES zips — use **`pyzipper`** instead.

Then it's a straight dictionary attack with any common-password list (the 2025 top-100
overlap heavily with all-time lists):

```python
import pyzipper
with pyzipper.AESZipFile("pw.zip") as z:
    for pw in wordlist:
        try:
            data = z.read("flag.txt", pwd=pw.encode())
            if b"LITCTF" in data: print(pw, data); break
        except Exception: pass
```

The password is **`1234qwer`** (a perennial top-list entry), which unlocks:

```
LITCTF{password_123456_103flkj3}
```

## Flag

```
LITCTF{password_123456_103flkj3}
```
