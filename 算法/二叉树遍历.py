

class TreeNode:
    def __init__(self,val):
        self.val=val
        self.left=None
        self.right=None

pre = input()

def buildTree(s):
    idx = 0
    def dfs():
        nonlocal idx 
        if idx >= len(s):
            return None 
        ch = s[idx]
        idx+=1
        if ch=="#":
            return None 
        root = TreeNode(ch)
        root.left = dfs()
        root.right = dfs()
        return root
    return dfs()

root = buildTree(pre)

def solve(node):
    if not node:
        return ""
    return solve(node.left)+node.val+solve(node.right)

print(solve(root))

