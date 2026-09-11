class Solution:
    def findEvenNumbers(self, digits: List[int]) -> List[int]:
        digits_count = Counter(digits)
        def my_all(a, b):
            for i in a:
                if a[i] > b[i]:
                    return False    
            return True 
        res = []
        for i in range(100, 1000, 2):
            a = i // 100
            b = (i // 10) % 10
            c = i % 10
            need = Counter([a, b, c])
            tmp = 0
            # print(need, digits_count)

            if my_all(need, digits_count):
                res.append(i)
            # for i in need:
            #     print(i, need[i],digits_count[i])
            #     if need[i] < digits_count[i]:
            #         tmp += 1
            # if tmp == len(need):
            #     res += 1
        return res
        