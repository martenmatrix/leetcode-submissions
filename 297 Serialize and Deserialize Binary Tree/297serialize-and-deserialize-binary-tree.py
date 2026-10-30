# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """

        if root is None:
            return ""

        res = []

        def pre_order_traversal(node):
            if not node:
                res.append("null")
                return
            res.append(str(node.val))

            pre_order_traversal(node.left)
            pre_order_traversal(node.right)

        pre_order_traversal(root)

        return "|".join(res)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        if data == "":
            return None

        res = data.split("|")

        self.index = 0

        def derive_graph_from_pre_order_traversal():
            val = res[self.index]

            self.index += 1

            if val == "null":
                return None

            node = TreeNode(int(val))

            node.left = derive_graph_from_pre_order_traversal()
            node.right = derive_graph_from_pre_order_traversal()

            return node

        return derive_graph_from_pre_order_traversal()

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))