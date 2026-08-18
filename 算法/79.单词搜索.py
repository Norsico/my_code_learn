from typing import List
from collections import Counter


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        board_row = len(board)
        board_column = len(board[0])

        count = Counter()
        for i in board:
            count.update(i)
        word_count = Counter(word)

        for key in word_count:
            if count[key] < word_count[key]:
                return False
        
        if word_count[word[0]] > word_count[word[-1]]:
            word = word[::-1]

        def dfs(row, column, index):
            if index >= len(word):
                return True
            if row >= board_row or row < 0 or column >= board_column or column < 0:
                return False

            if board[row][column] != word[index] or board[row][column] == "#":
                return False
            
            tmp = board[row][column]
            board[row][column] = "#"
            
            up = dfs(row-1,column,index+1) # 上
            down = dfs(row+1,column,index+1) # 下
            left = dfs(row,column-1,index+1) # 左
            right = dfs(row,column+1,index+1) # 右
            
            if (up or down or left or right):
                return True

            # 回溯
            board[row][column] = tmp
        
        for i in range(board_row):
            for j in range(board_column):
                if board[i][j] == word[0]:
                    if dfs(i,j,0):
                        return True
        return False




if __name__ == '__main__':
    s = Solution()
    board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
    print(s.exist(board, "ABCCED"))

    # count = Counter("ABCCED")    
    # print(count)
    # for k in count:
    #     print(k)