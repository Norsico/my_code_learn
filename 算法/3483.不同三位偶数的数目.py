class Solution:
    def totalNumbers(self, digits: List[int]) -> int:
        len_digits = len(digits)
        path = []
        res_set = set()
        used = [False] * len_digits
        def backtrack(digit_list):

            if len(path) == 3:
                if path[0] != 0 and path[-1] % 2 == 0:
                    res_set.add(100*path[0]+10*path[1]+path[2])
                return 
            
            for i in range(len_digits):
                if used[i]:
                    continue
                path.append(digits[i])
                used[i] = True
                backtrack(digits)
                used[i] = False
                path.pop()

        backtrack(digits)
        print(res_set)
        return len(res_set)
