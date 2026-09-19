import sys




data= list(sys.stdin.read().split())

x = 0

while x < len(data):
    res = ""
    for i in data[x]:
        if "A"<=i<="Z":
            res += chr(ord('Z') - (ord(i) - ord('A')))
        elif "a"<=i<="z":
            res += chr(ord('z') - (ord(i) - ord('a')))
        else:
            res += i

    print(res)
    x+=1
