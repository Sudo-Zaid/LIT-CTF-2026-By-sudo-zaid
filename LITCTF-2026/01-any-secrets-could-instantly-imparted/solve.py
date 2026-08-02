#!/usr/bin/env python3
"""
LIT CTF 2026 — crypto — "Any Secrets Could Instantly Imparted"

Hints:
  * Title acrostic: Any Secrets Could Instantly Imparted  ->  A S C I I  -> ASCII
  * Tiger: "Et tu, Brute?"  -> Caesar cipher, and "Brute" -> brute force
  => Caesar shift applied to raw ASCII byte values (not just A-Z).

The known flag prefix "LITCTF{" anchors the shift: plain = cipher + 4.
"""

CIPHER = "HEP?PBw=O?EE)fQh-qo)_0/o0n)casks]y"   # trailing '.' in the chat is sentence punctuation

def caesar_ascii(text, shift):
    return ''.join(chr((ord(c) + shift) % 256) for c in text)

def main():
    # Brute force every shift; keep the one that yields the flag format.
    for shift in range(1, 256):
        dec = caesar_ascii(CIPHER, shift)
        if dec.startswith("LITCTF{") and dec.endswith("}"):
            print(f"[+] shift +{shift}: {dec}")

if __name__ == "__main__":
    main()
