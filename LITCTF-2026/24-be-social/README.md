# be social

**Category:** Misc (OSINT) · **Points:** ~150 · **Solves:** 100+ · **Author:** ethan

**Flag:** `LITCTF{os_1nt_success_4f2a58b9}`

## Challenge

> Our friend John might've been a little too careless this time...
> Wrap your flag with LITCTF{}.
> https://bsky.app/profile/jsmithf.bsky.social  ·  http://136.115.87.65:31781/
>
> **hint:** Bluesky itself is not the target… the profile is for reference only, and
> obtaining/cracking the login credentials of the profile user is not part of the challenge.

## OSINT (Bluesky, reference only)

`jsmithf.bsky.social` = **John Smith**, 2 posts:
- "Check out my dog **Cooper**! 😀"
- "Just celebrated my **birthday** today, **July 25**!"

## Target site

"Secrets Login": username fixed to **John**, a 4-digit **PIN**, then `/home` with a
**secret password** gate.

1. **PIN = `0725`** (John's birthday, MM DD) → `/home`.
2. **Secret password = `cooper`** (his dog's name, **lowercase**) → reveals the secret:

```
POST /home   password=cooper
   → <p>os_1nt_success_4f2a58b9</p>
```

Wrap it: **`LITCTF{os_1nt_success_4f2a58b9}`**.

## Gotchas (what ate my time)

- The site rate-limits `/` and `/home` to **1 req/s**, and the session expires quickly.
  Automated attempts collided with the limit and returned false **"Your password is
  incorrect"** pages — even for the *correct* `cooper`. Solving it through a real browser
  (or with careful ≥2 s spacing and 429-retries) reveals the secret.
- The avatar PNG contains a custom `deBG` chunk with `E79C6AD88C7AEFC4`. It is a
  **decoy** — the hint ("don't crack credentials") explicitly steers you away from
  treating it as a hash/password.
- Case matters: `Cooper` is rejected, `cooper` works.

## Flag

```
LITCTF{os_1nt_success_4f2a58b9}
```
