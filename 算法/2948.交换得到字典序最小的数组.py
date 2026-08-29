from typing import List


class Solution:
    def lexicographicallySmallestArray(self, nums: List[int], limit: int) -> List[int]:
        n = len(nums)
        arr = [(x,index) for index,x in enumerate(nums)]
        arr.sort(key=lambda p: p[0])
        values = [value for value,_ in arr]
        indices = [index for _,index in arr]
        print(values)
        print(indices)
        i = 0
        ans = [0] * n

        while i < n:
            start = i

            # 当前连通块中的原下标
            groupIndices = []

            # 当前连通块中的元素值
            groupValues = []

            while i < n and (i == start or values[i] - values[i - 1] <= limit):
                groupIndices.append(indices[i])
                groupValues.append(values[i])
                i += 1
            # print(groupIndices)
            # print(groupValues)
            groupIndices.sort()
            for index, value in zip(groupIndices, groupValues):
                print(index, value)
                ans[index] = value

        return ans


if __name__ == '__main__':
    s = Solution()
    s.lexicographicallySmallestArray(nums = [1,7,6,18,2,1], limit = 3)



