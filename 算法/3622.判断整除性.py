
class Solution:
    def checkDivisibility(self, n: int) -> bool:
        sub_num = [int(x) for x in str(n)]
        # print(sub_num)
        add_all = 0
        multi_all = 1
        for i in sub_num:
            add_all+=i
            multi_all*=i
        print(add_all)
        print(multi_all)
        sum_all = add_all + multi_all
        print(sum_all)
        print(n % sum_all)
        if n % sum_all == 0:
            return True
        return False



if __name__ == '__main__':
    s = Solution()
    s.checkDivisibility(99)


