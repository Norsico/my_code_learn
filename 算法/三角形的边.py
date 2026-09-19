import sys

data = list(map(int, sys.stdin.read().split()))



for i in range(0, len(data),3):
    # print(data[i],end=" ")
    a = data[i:i+3]
    print(a)


