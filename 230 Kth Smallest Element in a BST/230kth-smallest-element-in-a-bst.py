# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def kthSmallest(self, root: TreeNode | None, k: int) -> int:
        stack = []
        curr = root
        iteration = 0 

        while True:
            # traverse to the leftmost node which will be the smallest
            while curr:
                stack.append(curr)
                curr = curr.left
            
            # because curr is null when we stop the while loop
            curr = stack.pop()

            iteration += 1

            if iteration == k:
                return curr.val

            # otherwise have to select more, try right, otherwise curr will revert back to the parent because of the stack, if right is in there we will start the traversal from that node again as from root
            curr = curr.right





