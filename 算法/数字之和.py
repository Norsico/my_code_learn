import sys 


data = list(map(int, sys.stdin.read().split()))

def solve(s):
    if len(s) == 1:
        return s 
    res = sum(list(map(int, [x for x in s])))
    return res

for i in data:
    str_i = str(i)
    print(solve(str_i), solve(str(int(i)*int(i))))

