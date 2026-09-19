import sys


data = list(map(int, sys.stdin.read().split()))

i = 0 
myset = list() # 2 4 9 16 25 ...
for j in range(2,101):
    myset.append(j*j)
# print(myset)

while i < len(data):
    if data[i] == 0:
        break
    n = data[i]

    i+=1
    ok = False
    for j in myset:
        if ok:
            break
        if n % j == 0:
            ok = True
            # print(j, n)
            print("Yes")
    if not ok:
        print("No")


