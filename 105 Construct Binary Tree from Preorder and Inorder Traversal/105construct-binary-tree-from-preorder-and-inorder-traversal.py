# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, preorder: list[int], inorder: list[int]) -> TreeNode | None:
        # prob or does not matter here
        if not preorder and not inorder:
            return None

        root_val = preorder[0]
        root = TreeNode(root_val)
        divider = inorder.index(root_val)

        root.left = self.buildTree(preorder[1:divider+1], inorder[:divider])
        root.right = self.buildTree(preorder[divider + 1:], inorder[divider+1:])

        return root
