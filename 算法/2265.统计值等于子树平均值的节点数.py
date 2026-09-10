# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def averageOfSubtree(self, root: TreeNode) -> int:
        cur = root
        res = 0
        def dfs(node):
            nonlocal res
            if not node:
                return 1,0
            left,sum_left = dfs(node.left)
            right,sum_right = dfs(node.right)
            if not node.left and not node.right:
                # print(1)
                res+=1
                # print(1, node.val)
                return 1, node.val
            if not node.left and node.right:
                # print(int((sum_right+node.val)/right+1), node.val)
                if int((sum_right+node.val)/(right+1)) == node.val:
                    res += 1
                # print(right+1, sum_right+node.val)
                return right+1, sum_right+node.val
            if node.left and not node.right:
                # print(int((sum_left + node.val)/left+1), node.val)
                if int((sum_left + node.val)/(left+1)) == node.val:
                    res += 1
                # print(left+1, sum_left + node.val)
                return left+1, sum_left + node.val
            # print(int((node.val+sum_left+sum_right)/left+right+1), node.val)
            if int((node.val+sum_left+sum_right)/(left+right+1)) == node.val:
                res += 1
            # print(left+right+1, node.val+sum_left+sum_right)
            return left+right+1, node.val+sum_left+sum_right
        dfs(cur)
        return res
