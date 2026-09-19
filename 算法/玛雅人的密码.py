import sys
from collections import deque

N = int(input())

s = input()

mydeque = deque()


def swamp(s_, i_):
    pre = s_[:i_]
    tail = s_[i_ + 2 :]
    mid1 = s_[i_]
    mid2 = s_[i_ + 1]
    return pre + mid2 + mid1 + tail


str_set = set()

mydeque.append((s, 0))

while mydeque:
    item = mydeque.popleft()
    # 判断是否存在2012
    if "2012" in item[0]:
        print(item[1])
        break
    # 列变为鲸子
    for j in range(len(item[0]) - 1):
        a = swamp(item[0], j)
        if a not in str_set:
            str_set.add(a)
            mydeque.append((a,item[1]+1))
        # print(j, a, b)




