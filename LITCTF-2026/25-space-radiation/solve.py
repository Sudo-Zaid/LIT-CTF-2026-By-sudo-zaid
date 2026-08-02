#!/usr/bin/env python3
"""
LIT CTF 2026 - misc/space radiation
Solve: decode a stream of extended-Hamming(16,11) SECDED codewords,
correcting the single "space radiation" bit-flip in each word.

Flag: LITCTF{h4MM1nG-3Rr0r_C0rR3cT10N!}
"""

TRANSMISSION = (
    "84ea cc57 4906 d24c cebd 93a2 3508 b04d 8b8f 8731 bc5a 0675 "
    "8a39 4143 b443 9ec3 030b b014 7066 5c34 2c18 b151 cb44 823d"
)

# Non-power-of-two positions 1..15 carry the 11 data bits.
# Positions 1,2,4,8 are Hamming parity; position 0 is the SECDED overall parity.
DATA_POS = [p for p in range(1, 16) if p & (p - 1)]  # 3,5,6,7,9,10,11,12,13,14,15


def decode_word(word: int):
    """Return (11 data bits, corrected_flag) for one 16-bit codeword.

    Bit layout is MSB-first: Hamming position 0 = bit 15 (MSB) ... position 15 = bit 0 (LSB).
    """
    b = [(word >> (15 - i)) & 1 for i in range(16)]

    # Syndrome = XOR of the positions (1..15) that hold a 1.
    syndrome = 0
    for i in range(1, 16):
        if b[i]:
            syndrome ^= i

    corrected = False
    if syndrome != 0:            # single-bit error -> flip position `syndrome` back
        b[syndrome] ^= 1
        corrected = True

    return [b[p] for p in DATA_POS], corrected


def main():
    words = [int(w, 16) for w in TRANSMISSION.split()]

    bitstream = []
    fixed = 0
    for w in words:
        data, corrected = decode_word(w)
        bitstream += data
        fixed += corrected

    # Pack the 264 data bits MSB-first into 33 bytes.
    out = bytearray()
    for i in range(0, len(bitstream), 8):
        v = 0
        for bit in bitstream[i:i + 8]:
            v = (v << 1) | bit
        out.append(v)

    flag = out.decode()
    print(f"[+] corrected {fixed}/{len(words)} radiation-flipped words")
    print(f"[+] {len(out)} bytes recovered")
    print(f"[+] FLAG: {flag}")


if __name__ == "__main__":
    main()
