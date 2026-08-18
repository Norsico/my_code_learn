from typing import List


class Solution:
    def longestSubsequence(self, nums: List[int]) -> int:
        res = 0
        res_sum = 0
        for i in nums:
            res_sum += i
            res = res ^ i 
        if res == 0 and res_sum != 0:
            return len(nums)-1
        elif res_sum != 0:
            return len(nums)
        else:
            return 0

if __name__ == '__main__':
    s = Solution()
    nums = [0,0,0,0,2,0,0,0,0]
    res = s.longestSubsequence(nums)
    print(res)
