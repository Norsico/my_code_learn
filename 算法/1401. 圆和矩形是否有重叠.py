class Solution:
    def checkOverlap(self, radius: int, xCenter: int, yCenter: int, x1: int, y1: int, x2: int, y2: int) -> bool:
        min_x = xCenter
        min_y = yCenter

        if x1<xCenter<x2:
            min_x = xCenter
        if y1<yCenter<y2:
            min_y = yCenter
        
        if xCenter<x1:
            min_x = x1 
        if xCenter>x2:
            min_x = x2 
        if yCenter<y1:
            min_y = y1
        if yCenter>y2:
            min_y = y2

        dx = xCenter - min_x
        dy = yCenter - min_y

        return dx * dx + dy * dy <= radius * radius