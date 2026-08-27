
# 思路没问题，暴力思路。但会超时
class Solution:
    def lexGreaterPermutation(self, s: str, target: str) -> str:
        len_s = len(s)
        res = []
        path = []
        used = [False]*len_s

        def backtrack():
            if len(path) == len_s:
                res.append(''.join(path))
            for i in range(len_s):
                if used[i]:
                    continue
                path.append(s[i])
                used[i] = True
                backtrack()
                path.pop()
                used[i] = False

        backtrack()
        res = list(set(res))
        my_res = []
        # print(res)
        for i in res:
            if i > target:
                my_res.append(i)

        return min(my_res) if my_res else ""

if __name__ == '__main__':
    solution = Solution()
    s = "abc"
    target = "bba"
    res = solution.lexGreaterPermutation(s, target)
    print(res)



# 贪心+回溯剪枝。没看懂

from collections import Counter

class Solution:
    def lexGreaterPermutation(self, s: str, target: str) -> str:
        n = len(s)
        cnt = Counter(s)          # 可用字符频率
        target = list(target)     # 方便索引

        def build_greater(pos: int, prefix: list, equal_so_far: bool) -> str:
            """
            pos: 当前构造的位置
            prefix: 已构造的字符列表
            equal_so_far: 前缀是否仍与 target 完全相等
            """
            if pos == n:
                # 如果全部相等，则不是大于，返回 None
                return None if equal_so_far else ''.join(prefix)

            # 如果前缀已经大于 target，后续直接填充最小剩余字符
            if not equal_so_far:
                # 剩余字符按升序排列
                remain = []
                for ch in sorted(cnt.keys()):
                    remain.append(ch * cnt[ch])
                return ''.join(prefix) + ''.join(remain)

            # 前缀仍与 target 相等，尝试等于 target[pos]
            ch_eq = target[pos]
            if cnt.get(ch_eq, 0) > 0:
                cnt[ch_eq] -= 1
                prefix.append(ch_eq)
                res = build_greater(pos + 1, prefix, True)
                prefix.pop()
                cnt[ch_eq] += 1
                if res is not None:
                    return res

            # 等于失败，尝试大于 target[pos] 的最小字符
            for ch in sorted(cnt.keys()):
                if ch > target[pos] and cnt[ch] > 0:
                    cnt[ch] -= 1
                    prefix.append(ch)
                    # 此时前缀已经大于 target，剩余字符升序填充
                    remain = []
                    for c in sorted(cnt.keys()):
                        remain.append(c * cnt[c])
                    result = ''.join(prefix) + ''.join(remain)
                    prefix.pop()
                    cnt[ch] += 1
                    return result

            # 没有任何可行选择
            return None

        ans = build_greater(0, [], True)
        return ans if ans is not None else ""

if __name__ == '__main__':
    sol = Solution()
    print(sol.lexGreaterPermutation("abc", "bba"))  
