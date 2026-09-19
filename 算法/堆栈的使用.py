import sys


from collections import deque


mydeque = deque()

data = list(map(str, sys.stdin.read().split()))

x = 0

while x<len(data):
    n = int(data[x])
    x+=1

    for _ in range(n):
        if data[x]=='A':
            if mydeque:
                print(mydeque[-1])
            else:
                print('E')
            x+=1
        elif data[x] == 'P':
            mydata = int(data[x+1])
            x+=2
            mydeque.append(mydata)
        elif data[x] == 'O':
            x+=1
            if mydeque:
                mydeque.pop()
                







