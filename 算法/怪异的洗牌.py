from re import M
import sys
from collections import deque

my_deque = deque()

n, k = list(map(int, input().split()))
for i in range(1, n + 1):
    my_deque.append(i)


def shift(mdeque, k):
    pop_item = []
    for _ in range(k):
        tmp = mdeque.popleft()
        pop_item.append(tmp)
    for i in pop_item:
        mdeque.append(i)


def flip(mdeque):
    n = len(mdeque)
    pop_item = []
    if n % 2 != 0:
        c = int((n - 1) / 2)
        for _ in range(c):
            tmp = mdeque.popleft()
            pop_item.append(tmp)
        for i in pop_item:
            mdeque.appendleft(i)
    else:
        c = int(n / 2)
        for _ in range(c):
            tmp = mdeque.popleft()
            pop_item.append(tmp)
        for i in pop_item:
            mdeque.appendleft(i)
    
data = list(map(int, sys.stdin.read().split()))

i = 0
while i < k:
    cur = data[i]
    i += 1
    shift(my_deque, cur)
    flip(my_deque)
# res = " ".join([str(i)])
for i in my_deque:
    print(i,end=" ")
    





