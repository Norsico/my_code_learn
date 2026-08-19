from typing import List


class Solution:
    def maxNumberOfFamilies(self, n: int, reservedSeats: List[List[int]]) -> int:
        left = {2,3,4,5}
        middle = {4,5,6,7}
        right = {6,7,8,9}

        reserved_rows = {}

        for row,col in reservedSeats:
            reserved_rows.setdefault(row, set()).add(col)
        result = (n - len(reserved_rows)) * 2

        # 只处理存在预约座位的行
        # print(reserved_rows.values())
        for reserved in reserved_rows.values():
            # print(left, reserved, reserved & left)
            can_left = not reserved & left
            can_middle = not reserved & middle
            can_right = not reserved & right

            if can_left and can_middle and can_right:
                result += 2
            elif not can_left and not can_middle and not can_right:
                continue
            else:
                result += 1
        # print(result)
        return result

if __name__ == "__main__":
    s = Solution()
    n = 4
    reservedSeats = [[4,3],[1,4],[4,6],[1,7]]
    s.maxNumberOfFamilies(n, reservedSeats)
