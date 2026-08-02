# my first ctf

**Category:** Web · **Points:** 131 · **Solves:** 178 · **Author:** halp

**Flag:** `LITCTF{n1ce_w0rk_dsf3kw}`

## Challenge

> Your classic beginner CTF problem
> http://136.115.87.65:31771/

## Solution

View source. The page says *"there's a flag on this page! somewhere..."* and the flag
is sitting in an **HTML comment**:

```bash
curl -s http://136.115.87.65:31771/
```

```html
<body>
    there's a flag on this page! somewhere...
    good luck finding it!
    <!-- LITCTF{n1ce_w0rk_dsf3kw} -->
</body>
```

## Flag

```
LITCTF{n1ce_w0rk_dsf3kw}
```
