from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        len_row = len(grid)
        len_col = len(grid[0])
        res = 0
        def dfs(row, col):
            if (not (0<=row<len_row)) or (not (0<=col<len_col)):
                return
            if grid[row][col] == '0':
                return

            if grid[row][col] == '1':
                grid[row][col] = '0'

            dfs(row-1,col) # 上
            dfs(row+1,col) # 下
            dfs(row,col-1) # 左
            dfs(row,col+1) # 右
        
        for i in range(len_row):
            for j in range(len_col):
                if grid[i][j] == '1':
                    dfs(i,j)
                    res += 1
        return res
