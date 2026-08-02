#!/usr/bin/env python3
"""
LIT CTF 2026 — crypto/misc — "faulty image 1 haha"

A tampered PNG that won't open. The PNG signature + IHDR are intact (400x150, RGB8,
IHDR CRC valid) so the geometry is fine, but the IDAT stream is broken.

Diagnosis:
  * The bytes "haha" (68 61 68 61) appear at offsets 100, 204, 308, ... -> a fixed
    period of 104 (also matching the challenge text, which is full of "haha").
  * i.e. the tamperer INSERTED "haha" after every 100 original bytes.

Fix: walk the file in 104-byte blocks, keep the first 100 bytes of each, drop the
4-byte "haha" tail. That reproduces the original file exactly: the recovered IDAT
decompresses to 150 * (1 + 400*3) = 180150 bytes with zero leftover.
"""
import zlib, struct, os

SRC = os.path.join(os.path.dirname(__file__), "corrupt.png")
OUT = os.path.join(os.path.dirname(__file__), "recovered.png")

def chunk(typ, payload):
    return struct.pack(">I", len(payload)) + typ + payload + \
           struct.pack(">I", zlib.crc32(typ + payload) & 0xffffffff)

def main():
    data = open(SRC, "rb").read()

    # Remove the "haha" inserted every 104 bytes.
    orig = b"".join(data[i:i+100] for i in range(0, len(data), 104))

    assert orig[:8] == b"\x89PNG\r\n\x1a\n"
    w, h = struct.unpack(">II", orig[16:24])
    ln = struct.unpack(">I", orig[33:37])[0]          # IDAT length
    raw = zlib.decompress(orig[41:41+ln])
    assert len(raw) == h * (1 + w * 3), "unexpected raw size"

    # Rebuild a clean PNG.
    png = b"\x89PNG\r\n\x1a\n" + orig[8:33] + \
          chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    open(OUT, "wb").write(png)
    print(f"[+] {w}x{h} image recovered -> {OUT}")
    print("[+] open it: the flag is rendered as text -> LITCTF{y0u_f1x3d_m3_85hf91j!}")

if __name__ == "__main__":
    main()
