class Solution:
    def reverseDegree(self, s: str) -> int:
        res = 0
        for i,item in enumerate(s):
            res+=(ord('z')-ord(item)+1)*(i+1)
        return res
        