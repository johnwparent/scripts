"""Increments an alphabetical string of scheme a,b,c,...,aa,ab,...,bcz
Note: currently only supports lowercase
"""

def inc(c):
    curr = ord(c[-1])
    over = curr // 122
    if over:
        return (inc(c[:-1]) if len(c[:-1]) else 'a') + 'a'
    return c[:-1] + chr(curr + 1)