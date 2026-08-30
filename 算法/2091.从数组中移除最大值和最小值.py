from typing import List


class Solution:
    def minimumDeletions(self, nums: List[int]) -> int:
        min_num = float('inf')
        min_index = 0
        max_num = -float('inf')
        max_index = 0
        len_nums = 0
        for index, num in enumerate(nums):
            len_nums+=1
            # print(index, num)
            if num >= max_num:
                max_num = num
                max_index = index
            if num <= min_num:
                min_num = num
                min_index = index
            # max_num = max(max_num,num)
        # print(max_index,max_num)
        # print(min_index,min_num)
        # print(len_nums-max_index)
        left_num_index = min(max_index,min_index)
        right_num_index = max(max_index,min_index)

        left_gap = left_num_index
        mid_gap = right_num_index-left_num_index-1
        right_gap = len_nums-right_num_index-1
        print(left_gap,mid_gap,right_gap) 

        return len_nums - max(left_gap,mid_gap,right_gap)


if __name__ == '__main__':
    s = Solution()
    nums = [2,10,7,5,4,1,8,6]
    print(s.minimumDeletions(nums))

