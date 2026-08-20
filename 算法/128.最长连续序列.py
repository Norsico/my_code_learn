from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        print(num_set)
        max_len = 0
        max_len_tmp = 0
        for num in num_set:
            if num-1 not in num_set:
                max_len_tmp = 1
                num_tmp = num
                while num_tmp+1 in num_set:
                    max_len_tmp+=1
                    num_tmp+=1
                max_len = max(max_len, max_len_tmp)
        return max_len


if __name__ == '__main__':
    s = Solution()
    nums = [0,-1,1,2,5]
    res = s.longestConsecutive(nums)
    print(res)
    
