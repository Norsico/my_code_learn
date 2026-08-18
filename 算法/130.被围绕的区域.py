from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        board_row_num = len(board)
        board_col_num = len(board[0])

        # print(board)

        def dfs (row, col, flag=False):
            if (not (0<= row <board_row_num)) or (not (0<= col <board_col_num)):
                return

            if board[row][col] in ('X', '#'):
                return
            if flag:
                board[row][col] = '#'

            if board[row][col] == 'O':
                board[row][col] = 'X'
                return
            if flag:
                dfs(row-1,col,True) # 上
                dfs(row+1,col,True) # 下
                dfs(row,col-1,True) # 左
                dfs(row,col+1,True) # 右
            else:
                dfs(row-1,col) # 上
                dfs(row+1,col) # 下
                dfs(row,col-1) # 左
                dfs(row,col+1) # 右 
        
        for y in range(board_col_num-1):
            if board[0][y] == 'O':
                dfs(0, y, True)
        for x in range(board_row_num-1):
            if board[x][board_col_num-1] == 'O':
                dfs(x, board_col_num-1, True)
        for y in range(board_col_num-1,0,-1):
            if board[board_row_num-1][y] == 'O':
                dfs(board_row_num-1, y, True)
        for x in range(board_row_num-1,0,-1):
            if board[x][0] == 'O':
                dfs(x, 0, True)

        if board_col_num == 1 and board_col_num == 1 and board[0][0] == 'O':
            dfs(0,0,True)

        for i in range(board_row_num):
            for j in range(board_col_num):
                if board[i][j] == 'O':
                    dfs(i,j)
                if board[i][j] == '#':
                    board[i][j] = 'O'

        print(board)

if __name__ == '__main__':
    s = Solution()
    board = [["O"]]
    s.solve(board)
