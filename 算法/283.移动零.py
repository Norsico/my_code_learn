from typing import List


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        zero_index = []
        for index, num in enumerate(nums):
            if num == 0:
                zero_index.append(index)
        zero_index = zero_index[::-1]
        len_zero = len(zero_index)
        for _ in range(len_zero):
            nums.append(0)
        for i in zero_index:
            del nums[i]

        # print(nums)

if __name__ == '__main__':
    s = Solution()
    nums = [0,1,0,3,12]
    s.moveZeroes(nums)
