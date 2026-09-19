import sys



data = list(map(int, sys.stdin.read().split()))

i = 0

while i < len(data):

    if data[i] == 0:
        break
    n = data[i]
    m = data[i+1]

    i += 2
    res = 1
    for k in range(n,n-m,-1):
        res *= k
    result = 0

    bin_str = str(bin(res))[::-1]

    for v in bin_str:

        if v != '1':
            result += 1
        else:
            break

    print(result)



