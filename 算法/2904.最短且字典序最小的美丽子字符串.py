from typing import Counter


class Solution:
    def shortestBeautifulSubstring(self, s: str, k: int) -> str:
        res = ""
        min_len = float('inf')
        for i in range(len(s)):
            for j in range(i, len(s)):
                # print(s[i:j+1])
                count = Counter(s[i:j+1])['1']
                if count == k:
                    # print(j-i+1)
                    if j-i+1 < min_len:
                        res = s[i:j+1]
                        min_len = j-i+1
                    if j-i+1 == min_len:
                        if s[i:j+1] < res:
                            res = s[i:j+1] 
                            min_len = j-i+1
                    # res.append(s[i:j+1])
        print(res)
        return res

if __name__ == '__main__':
    s = Solution()
    m_str = "111111110010001010"
    s.shortestBeautifulSubstring(m_str,11)


# print("a"<"bcde")
