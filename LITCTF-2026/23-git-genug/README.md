# git genug

**Category:** Misc (git forensics) · **Points:** 148 · **Solves:** 112 · **Author:** Ninjaprime

**Flag:** `LITCTF{r3fl0g_1s_y0ur_g1t_t1m3_m4ch1n3}`

## Challenge

> We accidentally leaked a secret in this repo at some point but we think we cleaned it
> up before pushing. Can you prove us wrong?

(`git genug` ≈ "git enough" — German *genug* = "enough".)

## Recon

`git log --all --oneline` shows a tempting commit:

```
2cad4d5 WIP flag stuff (probably not needed)     (branch feature/flag-thing)
```

…but that's a **decoy**:

```
NOTES.txt:  Just kidding, this isn't it either.
            LITCTF{n0t_th3_r34l_fl4g_k33p_l00k1ng}
```

So the real secret was committed and *removed*. `git fsck --unreachable` shows nothing,
but the removed commit still lives in the **reflog** / loose objects.

## Solution — the reflog is the time machine

`git reflog --all` exposes a commit that was `reset --hard` away:

```
f1c1c0c main@{3}: reset: moving to HEAD~1
e5ed944 main@{4}: commit: Add local dev notes (oops, forgot to gitignore)   <-- reset away
```

Show that orphaned commit (or just dump every object):

```bash
git show e5ed944
#   +++ b/secret.txt
#   TODO: remove before pushing
#   LITCTF{r3fl0g_1s_y0ur_g1t_t1m3_m4ch1n3}

# equivalently, grep all objects (loose + packed + dangling):
git cat-file --batch-all-objects --batch | grep -aoE "LITCTF\{[^}]*\}"
```

They committed `secret.txt` in `e5ed944`, then `git reset --hard HEAD~1` to erase it —
but the object is still recoverable via the reflog. *Reflog is your git time machine.*

## Flag

```
LITCTF{r3fl0g_1s_y0ur_g1t_t1m3_m4ch1n3}
```
