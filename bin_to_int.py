"""Script composing an adjacet string of binary values to integer representation"""
import sys

def compose_bin(bin):
    """Return numeric value of concatenated adjacent bytes"""
    p = 0
    for count, c in enumerate(bin[::-1]):
        root_c = c
        for _ in range(count*2):
            root_c = root_c << 8
        p = p + root_c
    return p


if __name__ == "__main__":
    print(compose_bin(sys.argv[1]))