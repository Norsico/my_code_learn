# n = 2019
# a = n % 1000
# n = n // 1000
# print(a, n)
class Solution:
    def countCommas(self, n: int) -> int:
        res = 0
        if n < 999 :
            return 0
        
        return n-999