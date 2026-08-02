#!/usr/bin/env python3
"""
LIT CTF 2026 — misc — "introduction" ("Were you paying attention?")

Not a code challenge — an OSINT / read-the-intro puzzle. The flag is split in two:

  * FIRST half  — hidden on the LIT 2026 Opening Ceremony slides, on the
    "Reminder / Join Our Discord" slide:   LITCTF{w3R3-Y0u-
    (followed by "nope nope nope / join the discord server! / not here")

  * SECOND half — quietly appended after the slides link in the CTF-start
    #announcements message on Discord:     p4Y1nG-4tT3nT10n?}

(The slide's "ex: LITCTF{W3-L0V3-PR0GR4MM1NG}" is just the example format = decoy.)
"""
slides_half  = "LITCTF{w3R3-Y0u-"
discord_half = "p4Y1nG-4tT3nT10n?}"
flag = slides_half + discord_half
print(flag)                      # LITCTF{w3R3-Y0u-p4Y1nG-4tT3nT10n?}
assert flag == "LITCTF{w3R3-Y0u-p4Y1nG-4tT3nT10n?}"
