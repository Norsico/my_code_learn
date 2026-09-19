import sys

import heapq

def main():
    data = sys.stdin.read().split()

    i = 0
    res = 0
    while i < len(data):
        n = int(data[i])
        i+=1
        if n == 0:
            break
        fruits = list(map(int, data[i:i+n]))
        i += n
        heapq.heapify(fruits)
        while len(fruits) > 1:
            a = heapq.heappop(fruits)
            b = heapq.heappop(fruits)
            sum_ = a+b
            res += sum_
            heapq.heappush(fruits, sum_)
    print("@@")
    print(res)

main()
