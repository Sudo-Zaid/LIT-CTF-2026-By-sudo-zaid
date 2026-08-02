#!/usr/bin/env python3
"""
LIT CTF 2026 — misc — "kcufniarb"

"kcufniarb" = "brainfuck" reversed. The given program is brainfuck with every
instruction MIRRORED to its opposite:
    <->>,  +<->-,  [<->],  .<->,
(Tell-tale: the source starts with ']' before any '[' — flipping the brackets makes it
balanced.) Un-mirror each character, then run as normal brainfuck; the ',' become '.'
so it prints output.
"""
SRC = ("----------]<-----<-----------<--------<------->>>>+[<<<++++,+++,-----------,"
       "<+++,>,<---,>>-------------,+++++++,+++++++++++,++++++++++,-----,-----,+++++,"
       "+++++,-------------------,---,++++++,----------,<-----------,>>,-,-,<+++++++,"
       "++++++++,-------------,<--,---,-----------,>>,<<++++++,>>+,<------,")
SWAP = {'<':'>','>':'<','+':'-','-':'+','[':']',']':'[','.':',',',':'.'}

def run(code):
    tape=[0]*30000; p=i=0; out=bytearray()
    stk=[]; m={}
    for j,c in enumerate(code):
        if c=='[': stk.append(j)
        elif c==']': k=stk.pop(); m[j]=k; m[k]=j
    while i < len(code):
        c=code[i]
        if   c=='>': p+=1
        elif c=='<': p-=1
        elif c=='+': tape[p]=(tape[p]+1)&0xff
        elif c=='-': tape[p]=(tape[p]-1)&0xff
        elif c=='.': out.append(tape[p])
        elif c=='[' and tape[p]==0: i=m[i]
        elif c==']' and tape[p]!=0: i=m[i]
        i+=1
    return bytes(out)

def main():
    code = "".join(SWAP.get(c, c) for c in SRC)   # un-mirror
    print("[+]", run(code).decode())

if __name__ == "__main__":
    main()
