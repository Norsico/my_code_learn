from typing import List


class Solution:
    def stoneGameV(self, stoneValue: List[int]) -> int:
        stone_num = len(stoneValue)
        dp = [[0]*stone_num for _ in range(stone_num)]
        prefix = [0]*(stone_num+1)
        for value in range(stone_num):
            prefix[value+1] = prefix[value+1] + prefix[value] + stoneValue[value]
        # print(prefix)
        for length in range(2,stone_num+1):
            # print(length) # 2 3 4 5 6
            for i in range(stone_num-length+1):
                # print(i,i+length-1) # 区间
                # print(length-1)
                best = 0
                for k in range(length-1):
                    left_sum=prefix[i+k+1]-prefix[i] # i ~ i+k
                    # print(i, i+k) # 左区间
                    right_sum=prefix[i+length]-prefix[i+k+1] # i+k+1 ~ i+length-1
                    # print(i+k+1, i+length-1) # 右区间
                    # print(left_sum, right_sum)
                    # if k == 1:
                        # print(best)
                    # print(left_sum,right_sum, best,i,i+k)                        
                    if left_sum > right_sum:
                        best = max(best, right_sum + dp[i+k+1][i+length-1])
                    elif left_sum < right_sum:
                        best = max(best, left_sum + dp[i][i+k])
                    else:
                        best = max(best, left_sum + dp[i][i+k], right_sum + dp[i+k+1][i+length-1])
                        

                    # dp[i][i+k]
                dp[i][i+length-1] = best
        # print(dp)
        return dp[0][-1]
                # for j in range(length-1):
                    
            # print("@")



if __name__ == "__main__":
    s = Solution()
    stoneValue = [6,2,3,4,5,5]
    # 0 1 0 
    # 0 0 1
    # 0 0 0
    res = s.stoneGameV(stoneValue=stoneValue)
    print(res)

        
