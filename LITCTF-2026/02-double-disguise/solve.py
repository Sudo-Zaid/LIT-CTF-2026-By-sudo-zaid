#!/usr/bin/env python3
"""
LIT CTF 2026 — crypto — "Double Disguise"

Two layers ("double disguise"):
  1. Base64  (trailing '==' is the tell)
  2. Single-byte XOR

The XOR key is recovered for free by XORing the base64-decoded bytes against the
known plaintext prefix "LITCTF{" -> every position yields 0x2A, so it's a constant
single-byte key.
"""
import base64

CT = "ZmN+aX5sUWwbTEt1fRpYRk51SV9aVw=="

def main():
    raw = base64.b64decode(CT)

    # Layer 2: derive the single-byte XOR key from the known flag prefix.
    key = raw[0] ^ ord("L")                       # 0x2A
    assert all((raw[i] ^ key) == c for i, c in enumerate(b"LITCTF{"))

    flag = bytes(b ^ key for b in raw).decode()
    print(f"[+] xor key = {key:#04x}")
    print(f"[+] flag    = {flag}")

if __name__ == "__main__":
    main()
