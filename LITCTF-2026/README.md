# LIT CTF 2026 — Writeups

Solved challenges from **LIT CTF 2026** (jeopardy-style, 48 hours), played solo.
Each challenge gets its own folder with a full writeup (`README.md`) and the working solve script (`solve.py` / `exploit.py` / notes).

| # | Challenge | Category | Flag | Key techniques |
|---|-----------|----------|:----:|----------------|
| 01 | [Any Secrets Could Instantly Imparted](01-any-secrets-could-instantly-imparted/) | Crypto | ✅ | Title acrostic → **ASCII**; "Et tu, Brute?" → **Caesar** brute force over raw ASCII bytes (shift +4) |
| 02 | [Double Disguise](02-double-disguise/) | Crypto | ✅ | Two layers: **Base64** then **single-byte XOR** (key `0x2A`), recovered from the `LITCTF{` prefix |
| 03 | [faulty image 1 haha](03-faulty-image-1/) | Crypto / Misc | ✅ | Tampered PNG: `haha` inserted every 100 bytes (period 104) broke IDAT; strip markers → rebuild → flag rendered in image |
| 04 | [faulty image 3](04-faulty-image-3/) | Crypto / Stego | ✅ | Decoy flag in image; real flag in **top-border** pixels (every 7px), color `(R,R+13,2R)` → **red channel = ASCII** |
| 05 | [faulty image 4](05-faulty-image-4/) | Crypto / Stego | ✅ | Pixels with blue `<16` (4-bit clipped) sit at **prime x-positions** in row 0; pack blue nibbles 2/byte → flag ("prime nibbles") |
| 06 | [extremely original](06-extremely-original/) | Crypto | ✅ | Leak is **not** b64-of-bytes (non-zero pad bits) → 34 six-bit **symbols**; XOR keystream = **LCG mod 64** (`21k+27`, k₀=35), brute all 64³ triples against the `LITCTF` crib |
| 07 | [introduction](07-introduction/) | Misc / OSINT | ✅ | Flag split: half in opening-ceremony **slides** (`LITCTF{w3R3-Y0u-`), half in the Discord CTF-start **announcement** (`p4Y1nG-4tT3nT10n?}`) |
| 08 | [long division](08-long-division/) | Pwn | ✅ | `INT_MIN / -1 = 2147483648` overflows int32; inputs validated but 64-bit division result fails the range check → program calls `win()` |
| 09 | [secrets](09-secrets/) | Pwn / Format string | ✅ | `printf(buf)` fmt-string ("behind the scenes" = printf); flag pre-loaded on stack, leak via `%14$p`–`%18$p` |
| 10 | [spiderman](10-spiderman/) | Pwn | ✅ | `gets` overflow (32B) overwrites a **function pointer** with `win` (0x4011f6, non-PIE) → ret2win |
| 11 | [greeter](11-greeter/) | Pwn | ✅ | `greet2` `gets()` stack overflow (offset 72) → overwrite return addr with `win` (0x401236, non-PIE) ret2win |
| 12 | [key](12-key/) | Pwn | ✅ | PIE, but `printf("Key: %p",&win)` leaks `win`; `gets` overflow (offset 40) overwrites "bread" return with `win`=`system("/bin/sh")` (+ret align) |
| 13 | [cellular automaton](13-cellular-automaton/) | Rev | ✅ | 32-gen **Rule 90** (cyclic, 208 bits) is linear over GF(2); invert via Gaussian elim, pin with `LITCTF{` prefix (rank 192→208) |
| 14 | [sequence lock](14-sequence-lock/) | Rev | ✅ | `LITCTF{`+20+`}`; running XOR `state^=(fib[i]+inner[i])&0xff` (init 0xAA) vs 20-byte target → invert per byte |
| 15 | [pathfinder](15-pathfinder/) | Rev | ✅ | Wants a **Dyck path** (35 `(`+35 `)`); `SUM += f[A+1][C]` per `)` = lex **rank** = `1337133713371337133`; unrank it |
| 16 | [my first ctf](16-my-first-ctf/) | Web | ✅ | Flag in an HTML source comment (view-source) |
| 17 | [cookie monster](17-cookie-monster/) | Web | ✅ | Role read from unsigned `role` cookie → forge `role=admin` (flag emitted literally as `flag{...}`) |
| 18 | [color palette](18-color-palette/) | Web | ✅ | 8 SVG `#RRGGBB` fills = 3 ASCII bytes each; concatenate in order → flag |
| 19 | [world cup chat](19-world-cup-chat/) | Web | ✅ | Double-encoded entity gives `offset=67`; subtract 67 from `&#NNN;` codes across elements |
| 20 | [image fetcher](20-image-fetcher/) | Web / SSRF | ✅ | `/fetch?url=` SSRF → scan `127.0.0.1:5000-6000`; port 5050 decoy, flag on port 5267 |
| 21 | [pw.zip](21-pw-zip/) | Misc | ✅ | WinZip **AES-256** zip (needs `pyzipper`); dictionary attack → password `1234qwer` |
| 22 | [kcufniarb](22-kcufniarb/) | Misc | ✅ | Mirror-image **brainfuck** (`<`↔`>`,`+`↔`-`,`[`↔`]`,`,`↔`.`); un-mirror → run → flag |
| 23 | [git genug](23-git-genug/) | Misc | ✅ | Decoy flag in a branch; real secret in a `reset --hard`'d commit — recover via `git reflog` / all-objects |
| 24 | [be social](24-be-social/) | Misc / OSINT | ✅ | Bluesky OSINT: PIN=birthday `0725`, `/home` secret password = dog's name `cooper` (lowercase); avatar `deBG` hex was a decoy |
| 24 | [be social](24-be-social/) | Misc / OSINT | ✅ | Birthday→PIN `0725`; secret leaked in avatar's **original PNG metadata** (`deBG` chunk via PDS `getBlob`) |
| 25 | [space radiation](25-space-radiation/) | Misc | ✅ | 24× **extended Hamming(16,11) SECDED** words; syndrome = flipped-bit address → correct 20/24 radiation flips, pack 11 data bits/word → 33-byte flag |

## Layout

```
NN-challenge-name/
├── README.md      # writeup: recon → vulnerability → exploitation → flag
├── solve.py       # working solve script
└── files/         # provided challenge files (when small enough to commit)
```

## Toolbox

Standard offensive/CTF Python tooling — `pwntools`, `pycryptodome`, `requests`, `z3-solver`,
`sympy`, `capstone`, plus the usual CLI kit (`binwalk`, `strings`, `xxd`, `ghidra`, `wireshark`).

---

*Writeups are published after the CTF ends.*
