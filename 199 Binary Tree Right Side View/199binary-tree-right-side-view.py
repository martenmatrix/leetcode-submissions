# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

from collections import deque

class Solution:
    def rightSideView(self, root: TreeNode | None) -> list[int]:
        if not root:
            return []

        curr_lvl = deque([root])
        res = []

        while curr_lvl:
            most_right = curr_lvl[-1]
            res.append(most_right.val)

            for node in curr_lvl.copy():
                curr_lvl.popleft()
                # left has to be added first, so rightmost value stays at the end
                if node.left:
                    curr_lvl.append(node.left)
                if node.right:
                    curr_lvl.append(node.right)
            
        return res


        