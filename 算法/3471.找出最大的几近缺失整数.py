from typing import List


class Solution:
    def largestInteger(self, nums: List[int], k: int) -> int:
        if len(nums) == k:
            return max(nums)
        sub = []
        for i in range(0,len(nums)-k+1):
            # print(i)
            sub.append(nums[i:i+k])
        # print(sub)
        set_nums = set(nums)
        res_dic = {}
        for i in set_nums:
            for j in sub:
                if i in set(j):
                    if res_dic.get(i):
                        res_dic[i] += 1
                    else:
                        res_dic[i] = 1
        # print(res_dic)
        res = []
        for j in res_dic:
            if res_dic[j] == 1:
                res.append(j)
        return max(res) if res else -1

if __name__ == "__main__":
    s = Solution()
    nums = [0,0]
    k = 1
    res = s.largestInteger(nums,k)
    print(res)

