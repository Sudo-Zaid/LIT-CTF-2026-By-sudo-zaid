# introduction

**Category:** Misc (OSINT) · **Points:** 66 · **Solves:** 13 · **Author:** joshadoodle

**Flag:** `LITCTF{w3R3-Y0u-p4Y1nG-4tT3nT10n?}`

## Challenge

> Were you paying attention?

No file, no service — the whole challenge is the question. The flag was hidden across
the CTF's own **introduction materials**, and it's deliberately **split in two**.

## Solution

### Half 1 — the opening-ceremony slides

The CTF-start `#announcements` message links the *LIT 2026 Opening Ceremony* slides with
"*Make sure to watch it if you haven't yet!*". Exporting the public deck as text
(`/presentation/d/<id>/export/txt`) and reading the **"Reminder / Join Our Discord"**
slide gives:

```
discord.gg/k6yzFdZ
LITCTF{w3R3-Y0u-
nope nope nope
join the discord server!
not here
```

So the slide holds the **first half** — `LITCTF{w3R3-Y0u-` — and literally tells you the
rest is "*not here… join the discord server!*".

> An earlier slide shows `Submitted as text, ex: LITCTF{W3-L0V3-PR0GR4MM1NG}` — that's
> just the **example** flag format, a decoy.

### Half 2 — the Discord announcement

Back in Discord, the message that opened the CTF round (from **joshadoodle**) ends with
the opening-ceremony slides link… and then a stray fragment tacked on right after it:

```
… Here are the slides for our opening ceremony yesterday. Make sure to watch it if you
haven't yet! https://docs.google.com/presentation/d/1Zz…rxqtk/edit?usp=sharing p4Y1nG-4tT3nT10n?}
```

That trailing `p4Y1nG-4tT3nT10n?}` is the **second half**.

### Combine

```
LITCTF{w3R3-Y0u-   +   p4Y1nG-4tT3nT10n?}
= LITCTF{w3R3-Y0u-p4Y1nG-4tT3nT10n?}
```

Leetspeak for **"were you paying attention?"** — you had to actually watch the opening
ceremony *and* read the CTF-start announcement to the very end.

## Flag

```
LITCTF{w3R3-Y0u-p4Y1nG-4tT3nT10n?}
```
