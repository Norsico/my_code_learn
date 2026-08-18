class Solution:
    def maximumLengthSubstring(self, s: str) -> int:
        left = 0
        hash_table = {}
        max_len = 0
        for right in range(len(s)):
            if not hash_table.get(s[right]):
                hash_table[s[right]] = 1
                max_len = max(max_len, right-left+1)
            else:
                
                hash_table[s[right]] += 1
                if hash_table[s[right]] > 2:
                    while s[left] != s[right]:
                        hash_table[s[left]] -= 1
                        left+=1
                    hash_table[s[left]] -= 1
                    left+=1
                else:
                    max_len = max(max_len, right-left+1)
        print(max_len)
        return max_len

if __name__ == "__main__":
    solution = Solution()
    s = "aaaa"
    solution.maximumLengthSubstring(s)
