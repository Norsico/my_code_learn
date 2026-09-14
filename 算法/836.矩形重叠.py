from typing import List


class Solution:
    def isRectangleOverlap(self, rec1: List[int], rec2: List[int]) -> bool:
        a1x,a1y, a2x, a2y = rec1

        b1x,b1y, b2x, b2y = rec2

        if a1x==a2x or a1y == a2y or b1x == b2x or b1y == b2y:
            return False
        if (
            a2x<=b1x or
            a2y<=b1y or
            b2x<=a1x or
            b2y<=a1y
        ): return False
        return True
