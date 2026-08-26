from typing import List,Counter

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        mydict = dict()
        for item in strs:
            sorted_item = "".join(sorted(item))
            # print(sorted(item))
            if sorted_item not in mydict:
                mydict[sorted_item] = [item]
            else:
                mydict[sorted_item].append(item)
        print(list(mydict.values()))
        return list(mydict.values())
if __name__ == '__main__':
    solution = Solution()
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    solution.groupAnagrams(strs)


# m = {
#     "a":[],
#     "b":[23]
# }
# if "c" in m and m["a"]:
#     print(123)