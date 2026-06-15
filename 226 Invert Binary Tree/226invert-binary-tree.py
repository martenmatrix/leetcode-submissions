# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # what exactly is root, and why is it represented like an array
        if not root:
            return root

        oldLeft = root.left
        oldRight = root.right

        root.left = self.invertTree(oldRight)
        root.right = self.invertTree(oldLeft)

        return root
