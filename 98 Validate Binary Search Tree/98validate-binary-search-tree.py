from math import inf

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        if not root:
            return True

        # Contains each node and its lower and upper bounds.
        stack = [(root, -inf, inf)]

        while stack:
            curr, lower, upper = stack.pop()
            currVal = curr.val

            if not lower < currVal < upper:
                return False

            if curr.left:
                stack.append((curr.left, lower, currVal))

            if curr.right:
                stack.append((curr.right, currVal, upper))

        return True
