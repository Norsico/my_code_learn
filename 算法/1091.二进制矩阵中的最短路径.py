from collections import deque
from typing import List


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        if grid[0][0] != 0:
            return -1
        directions = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        len_row = len(grid)
        len_col = len(grid[0])
        if grid[len_row-1][len_col-1] != 0 or grid == [[0]]:
            return -1
        my_deque = deque()
        res = 1
        my_deque.append((0,0))
        while len(my_deque) != 0:
            len_deque = len(my_deque)
            for _ in range(len_deque):
                x, y = my_deque.popleft()
                grid[x][y] = 1
                for dx, dy in directions:
                    next_x, next_y = x+dx, y+dy
                    if (0<=next_x<=len_row-1) and (0<=next_y<=len_col-1):
                        if grid[next_x][next_y] == 0 and next_x == len_row-1 and next_y == len_col-1:
                            res += 1
                            return res 
                        # elif grid[next_x][next_y] == 0 and i == len_deque-1:
                        #     res += 1
                        #     my_deque.append((next_x,next_y))
                        elif grid[next_x][next_y] == 0 and not ((next_x,next_y) in my_deque):
                            my_deque.append((next_x,next_y))
            res += 1
        return -1 


if __name__ == "__main__":
     s = Solution()
     grid = [[0,1],[1,0]]
     print(s.shortestPathBinaryMatrix(grid))
        