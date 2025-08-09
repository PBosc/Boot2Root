string = "isrveawhobpnutfg"
alpha = "abcdefghijklmnopqrstuvwxyz"

def checkchar(c):
    ret = string[ord(c) & 0xf]
    return ret

for c in alpha:
    print(checkchar(c), c)
