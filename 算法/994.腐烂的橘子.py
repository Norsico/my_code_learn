from collections import deque
from typing import List
from collections import deque
from typing import List

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # 记录行列大小
        row = len(grid)
        col = len(grid[0])

        # 初始化队列
        my_deque = deque()
        # 初始化移动方向
        directions = [(1,0),(0,1),(-1,0),(0,-1)] # 右 上 左 下
        # 分钟数
        res = 0
        good = 0

        # 找到烂橘子和好橘子
        for x in range(row):
            for y in range(col):
                if grid[x][y] == 2:
                    my_deque.append((x,y))
                if grid[x][y] == 1:
                    good += 1
        if good == 0 and len(my_deque) == 0:
            return 0
        
        # 处理烂橘子
        while len(my_deque) != 0:
            res += 1
            len_deque = len(my_deque)
            # print(len_deque)
            for _ in range(len_deque):
                x, y = my_deque.popleft()
                for dx, dy in directions:
                    # 干净橘子
                    if (0<=x+dx<row and 0<=y+dy<col) and grid[x+dx][y+dy] == 1:
                        # 污染为腐烂橘子
                        grid[x+dx][y+dy] = 2
                        # 添加到队列中
                        my_deque.append((x+dx,y+dy))
        # 遍历查询是否全部污染
        for x in range(row):
            for y in range(col):
                # 仍然有新鲜橘子
                if grid[x][y] == 1:
                    return -1
        return res - 1

if __name__ == '__main__':
    s = Solution()
    grid = [[0]]
    print(s.orangesRotting(grid=grid))

