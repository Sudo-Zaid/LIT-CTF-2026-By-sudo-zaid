# kcufniarb

**Category:** Misc · **Points:** 142 · **Solves:** 127 · **Author:** halp

**Flag:** `LITCTF{ti_did_ruoy_234rjwado4i3}`

## Challenge

The title **`kcufniarb`** is **`brainfuck`** spelled backwards, and the body is a
brainfuck-looking program:

```
----------]<-----<-----------<--------<------->>>>+[<<<++++,+++,-----------,<+++,>,<---, ...
```

## Solution

Two tells that it's *mirror-image* brainfuck rather than plain BF:

1. It uses `,` (input) but no `.` (output) — yet a flag must be *printed*.
2. It contains `]` **before** any `[` — invalid bracket order for real BF.

So every instruction has been swapped with its opposite. Un-mirror each character:

```
<->>   +<->-   [<->]   .<->,
```

Now the `]…[` becomes a balanced `[…]`, and the `,` become `.` (output). Running the
un-mirrored program as normal brainfuck prints the flag:

```python
SWAP={'<':'>','>':'<','+':'-','-':'+','[':']',']':'[','.':',',',':'.'}
code="".join(SWAP.get(c,c) for c in SRC)
print(run_brainfuck(code))     # LITCTF{ti_did_ruoy_234rjwado4i3}
```

Fittingly for a reversed challenge, the message reads backwards:
`ti_did_ruoy` = "you did it".

## Flag

```
LITCTF{ti_did_ruoy_234rjwado4i3}
```
