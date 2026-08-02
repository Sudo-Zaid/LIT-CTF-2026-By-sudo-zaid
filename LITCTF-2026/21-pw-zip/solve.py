#!/usr/bin/env python3
"""
LIT CTF 2026 — misc — "pw.zip"

Password-protected zip; the author says the password is one of the 100 most-used
passwords of 2025. The archive uses **WinZip AES-256** (compress_type 99, extra field
'AE'x03), which Python's stdlib `zipfile` cannot decrypt -> use `pyzipper`.

Dictionary-attack it with a common-password list. Password: 1234qwer.
"""
import pyzipper, os

BIN = os.path.join(os.path.dirname(__file__), "pw.zip")

def main():
    # any common-password wordlist works; the 2025 top-100 overlap heavily with these
    words = [l.strip() for l in open("wl.txt", encoding="latin1")] if os.path.exists("wl.txt") \
            else ["1234qwer"]
    with pyzipper.AESZipFile(BIN) as z:
        for pw in words:
            try:
                data = z.read("flag.txt", pwd=pw.encode())
                if b"LITCTF" in data:
                    print(f"[+] password: {pw}")
                    print(f"[+] {data.decode().strip()}")
                    return
            except Exception:
                pass

if __name__ == "__main__":
    main()
