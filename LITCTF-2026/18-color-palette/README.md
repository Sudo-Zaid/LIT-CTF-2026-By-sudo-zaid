# color palette

**Category:** Web · **Points:** 136 · **Solves:** 152 · **Author:** joshadoodle

**Flag:** `LITCTF{n3w-fLAg-c0LOR!?}`

## Challenge

> Say hello to the new LIT logo colors! They will adorn our new flag. Don't you love
> the look?
> http://136.115.87.65:31774/

## Solution

The page is an SVG "logo" made of 8 triangles, each with a `fill` hex color:

```html
<polygon ... fill="#4c4954"/>
<polygon ... fill="#435446"/>
<polygon ... fill="#7b6e33"/>
<polygon ... fill="#772d66"/>
<polygon ... fill="#4c4167"/>
<polygon ... fill="#2d6330"/>
<polygon ... fill="#4c4f52"/>
<polygon ... fill="#213f7d"/>
```

A `#RRGGBB` color is just **3 bytes**. Reading each color as 3 ASCII characters (in
document order) spells the flag — the colors literally *adorn the flag*:

```
4c 49 54 = LIT   43 54 46 = CTF   7b 6e 33 = {n3   77 2d 66 = w-f
4c 41 67 = LAg   2d 63 30 = -c0   4c 4f 52 = LOR   21 3f 7d = !?}
```

```python
colors=["4c4954","435446","7b6e33","772d66","4c4167","2d6330","4c4f52","213f7d"]
print(b"".join(bytes.fromhex(c) for c in colors).decode())
# LITCTF{n3w-fLAg-c0LOR!?}
```

## Flag

```
LITCTF{n3w-fLAg-c0LOR!?}
```
