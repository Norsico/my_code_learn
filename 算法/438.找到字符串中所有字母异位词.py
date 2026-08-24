from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        len_s = len(s)
        len_p = len(p)
        p_dict = {}
        sub_s_dict = {}
        res = []
        def insert_dict(dict, n):
            if not dict.get(n):
                dict[n] = 1
            else:
                dict[n] += 1
        for i in p:
            insert_dict(p_dict, i)
        print(p_dict)
        left = 0
        for right in range(len_s):
            if s[right] in p_dict:
                if not sub_s_dict.get(s[right]):
                    sub_s_dict[s[right]] = 1
                    right+=1
                    if right-left+1 == len_p:
                        res.append(left)
                elif p_dict[s[right]] > sub_s_dict[s[right]]:
                    sub_s_dict[s[right]] += 1
                    right+=1
                    if right-left+1 == len_p:
                        res.append(left)
                else:
                    sub_s_dict[s[right]] += 1
                    right+=1
                    while sub_s_dict.get(s[right]) and p_dict[s[right]] <= sub_s_dict[s[right]]:
                        sub_s_dict[s[left]] -= 1
                        if sub_s_dict[s[left]] == 0:
                            del sub_s_dict[s[left]]
                        left += 1
                    if right-left+1 == len_p:
                        res.append(left)
                        
            else:
                left = right+1


                
            
        print(res)
            

if __name__ == '__main__':
    solution = Solution()
    s = "abab"
    p = "ab"
    solution.findAnagrams(s, p)
