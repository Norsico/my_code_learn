from re import finditer
import sys


data = list(map(int, sys.stdin.read().split()))

i = 0
fa = list()

def find(x):
    if fa[x] == x:
        return x 
    return find(fa[x])

def union(u,v):
    if find(u) != find(v):
        fa[find(u)] = find(v)

while i < len(data):
    if data[i] == 0:
        break
    n = data[i]
    fa = list(range(n+1))
    i+=1
    m = data[i]
    i+=1
    for _ in range(m):
        a = data[i]
        i+=1
        b = data[i]
        i+=1
        union(a,b)

    father = find(fa[1])
    print(fa, "fa")

    is_find = False
    for v in range(1, len(fa)):

        if find(v) != father:
            is_find = True
            print("NO")
            break
    if not is_find:
        print("YES")




