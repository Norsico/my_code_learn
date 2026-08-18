from typing import List


class Solution:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        left = 0 
        max_len = 0
        count_dic = {}
        # for item in nums:
        #     count_dic[item] = 0
        
        for right in range(len(nums)):
            if count_dic.get(nums[right]):
                count_dic[nums[right]] += 1
            else:
                count_dic[nums[right]] = 1

            if count_dic[nums[right]] > k:
                while nums[left] != nums[right]:
                    count_dic[nums[left]] -= 1
                    left+=1
                count_dic[nums[left]] -= 1
                left+=1
            else:
                max_len = max(max_len, right-left+1)


        return max_len


if __name__ == '__main__':
    s = Solution()
    nums = [1,2,2,2]
    res = s.maxSubarrayLength(nums, 1)
    print(res)


# nums = [1,2,3,1,2,3,1,2]
# count = Counter(nums)
# print(count) # Counter({1: 3, 2: 3, 3: 2})
# print(count[1]) # 3

# nums = [1,2,3]
# print(nums[0:0]) # []

# count_dic = {}
# for item in nums:
#     count_dic[item] = 0
# print(count_dic)

# count_dic[1] += 1
# print(count_dic)

# print(count_dic.get(1))