#!/usr/bin/env python3
"""
LIT CTF 2026 — misc/OSINT — "be social"

John (bsky.app/profile/jsmithf.bsky.social) was "too careless": he hid his secret in
his AVATAR's PNG metadata.

- Birthday "July 25" (post) -> the site's 4-digit PIN = 0725 (username John) -> /home,
  which gates "My biggest secret" behind a password.
- The secret itself was leaked in John's avatar: the CDN strips metadata, but the PDS's
  com.atproto.sync.getBlob returns the ORIGINAL upload. Parsing its PNG chunks reveals a
  non-standard `deBG` chunk containing the secret.

Flag = LITCTF{ <deBG value> } = LITCTF{E79C6AD88C7AEFC4}
"""
import urllib.request, struct

DID = "did:plc:2p5dk5wrpltk3zwkr6vkwns5"
PDS = "https://chalciporus.us-west.host.bsky.network"
AVATAR_CID = "bafkreiaonqqmshubrzu7yqiu5zsnjig5f26t6f252zvc2ikwul345pn5ka"

def main():
    url = f"{PDS}/xrpc/com.atproto.sync.getBlob?did={DID}&cid={AVATAR_CID}"
    png = urllib.request.urlopen(url, timeout=30).read()
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    i = 8
    while i < len(png) - 8:
        ln = struct.unpack(">I", png[i:i+4])[0]
        typ = png[i+4:i+8]
        data = png[i+8:i+8+ln]
        if typ not in (b"IHDR", b"IDAT", b"IEND", b"PLTE"):
            print(f"[+] non-standard chunk {typ.decode('latin1')}: {data!r}")
            secret = data.decode()
            print(f"[+] FLAG: LITCTF{{{secret}}}")
        i += 12 + ln
        if typ == b"IEND":
            break

if __name__ == "__main__":
    main()
