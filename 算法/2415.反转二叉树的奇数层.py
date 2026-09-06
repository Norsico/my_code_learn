# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def reverseOddLevels(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        my_deque = deque()
        if not root:
            return None
        my_deque.append(root)
        index = 0
        while my_deque:
            # print(index)
            
            tmp = my_deque.copy()
            tmp_num = []
            len_my_deque = len(my_deque)
            if index % 2 !=0:
                for _ in range(len(tmp)):
                    l = tmp.popleft()
                    # print(l.val)
                    tmp_num.append(l.val)
                # print(tmp_num)
                for i in range(len_my_deque):
                    l = my_deque.popleft()
                    # print(l.val)
                    if l.left:
                        my_deque.append(l.left)
                    if l.right:
                        my_deque.append(l.right)
                    l.val = tmp_num[len(tmp_num)-i-1]
            else:
                for _ in range(len_my_deque):
                    l = my_deque.popleft()
                    # print(l.val)
                    if l.left:
                        my_deque.append(l.left)
                    if l.right:
                        my_deque.append(l.right)
            # print(l.val)
            index +=1
        return root
        