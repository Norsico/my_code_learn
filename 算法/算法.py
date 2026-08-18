from typing import List

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        res = []
        path = []
        len_s = len(s)
        def backtrack(start_index):

            if start_index >= len(s):
                res.append(path.copy())
                return

            for i in range(start_index, len_s):
                if s[start_index:i+1] != s[start_index:i+1][::-1]:
                    continue
                path.append(s[start_index:i+1])
                backtrack(i+1)
                path.pop()

        backtrack(0)
        # print(res)
        return res
if __name__ == '__main__':
    solution = Solution()
    s = "aaba"
    res = solution.partition(s)
    print(res)
