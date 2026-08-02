# world cup chat

**Category:** Web · **Points:** 143 · **Solves:** 126 · **Author:** Ninjaprime

**Flag:** `LITCTF{ent1ty_m4g1c_1fj10d}`

## Challenge

> After the Brazil vs Morocco World Cup game… Vini Jr. and Achraf Hakimi were chatting
> about a secret flag for LIT. … The spy's words were encrypted in a very weird way.
>
> **hint:** Do you know what a unicode entity code is? Try using the unicode entity
> decimal code.

## Recon

The page source is full of **HTML numeric character entities** (`&#NNN;`):

```html
<p>Vini Jr.: &amp;#111;&amp;#102;&amp;#102;&amp;#115;&amp;#101;&amp;#116;=&amp;#54;&amp;#55;</p>
<p>Achraf Hakimi: &#143;&#140;&#151;&#134;&#151;&#137;&#190;&#168;&#177;&#183;&#116;&#183;&#188;</p>
<img src="soccer.jpg" alt="&#162;&#176;&#119;&#170;&#116;&#166;&#162;&#116;&#169;&#173;&#116;&#115;">
<p style="text-align: right;">&#167;&#192;</p>
```

**Vini's line is double-encoded** (`&amp;#111;` → `&#111;` → `o`). Decoding it twice
gives the key:

```
&#111;&#102;&#102;&#115;&#101;&#116; = &#54;&#55;   ->   offset=67
```

## Solution

The other three elements are single-encoded entities whose decimal codes are the message
shifted by **+67**. Subtract 67 from each and read the elements in document order:

```python
achraf = [143,140,151,134,151,137,190,168,177,183,116,183,188]  # "LITCTF{ent1ty"
img    = [162,176,119,170,116,166,162,116,169,173,116,115]       # "_m4g1c_1fj10"
rightp = [167,192]                                               # "d}"
print("".join(chr(c-67) for c in achraf+img+rightp))
# LITCTF{ent1ty_m4g1c_1fj10d}
```

## Flag

```
LITCTF{ent1ty_m4g1c_1fj10d}
```
