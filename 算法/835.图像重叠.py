from typing import List 


class Solution:
    def largestOverlap(self, img1: List[List[int]], img2: List[List[int]]) -> int:
        n = len(img1[0])
        res = 0
        def find_overlap(matrix1, matrix2):
            overlap = 0
            for i in range(n):
                for j in range(n):
                    if matrix1[i][j] == 1 and matrix1[i][j] == matrix2[i][j]:
                        overlap+=1
            return overlap
        
        directions = []

        matrix = [[0]*(3*n-2) for _ in range(3*n-2)]

        for i in range(n-1, 2*n-1):
            for j in range(n-1, 2*n-1):
                matrix[i][j] = img1[i-n+1][j-n+1]
        # print(matrix[4][3])
        for i in range(0,2*n-1):
            for j in range(0,2*n-1):
                # cur = matrix[i:i+n][j:j+n]
                cur = [row[j:j+n] for row in matrix[i:i+n]]
                res = max(res, find_overlap(cur, img2))
        return res

