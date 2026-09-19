from typing import List


class Solution:
    def minSumOfLengths(self, arr: List[int], target: int) -> int:
        n = len(arr)
        left = 0
        total = 0
        res = []   # 存放所有和为 target 的区间 (left, right)

        # 1. 滑动窗口收集所有合法区间
        for right, x in enumerate(arr):
            total += x
            while total > target:
                total -= arr[left]
                left += 1
            while total == target:
                res.append((left, right))
                total -= arr[left]
                left += 1
        print(res)
        # 2. 用 best 数组记录到每个位置为止，出现过的最短合法子数组长度
        INF = float('inf')
        best = [INF] * n

        for l, r in res:
            length = r - l + 1

            best[r] = length
        print(best)
        # 前缀最小值：best[i] 表示到位置 i 为止（包括 i）的最短长度
        for i in range(1, n):
            if best[i-1] < best[i]:
                best[i] = best[i-1]
        print(best)
        # 3. 遍历每个区间，尝试与左边的合法区间配对
        ans = INF
        for l, r in res:
            length = r - l + 1
            if l > 0 and best[l-1] != INF:
                ans = min(ans, best[l-1] + length)

        return ans if ans != INF else -1

if __name__ =="__main__":
    # 可以在这里添加测试代码
    solution = Solution()
    arr = [1,0,2,1,1,5,1,3,1]
    target = 3
    print(solution.minSumOfLengths(arr, target))


