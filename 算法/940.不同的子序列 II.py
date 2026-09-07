from functools import lru_cache

class Solution:
    def distinctSubseqII(self, s: str) -> int:
        MOD = 10**9 + 7
        n = len(s)
        # 预处理每个位置的上一次出现位置
        prev = [-1] * n
        last_pos = {}
        for i, ch in enumerate(s):
            prev[i] = last_pos.get(ch, -1)
            last_pos[ch] = i
        print(prev)


if __name__ == '__main__':
    s = "abcabcaaabbcc"
    solution = Solution()
    result = solution.distinctSubseqII(s)
    print(result)  # 输出结果
