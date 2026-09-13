"""
# Definition for a Node.
class Node(object):
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

class Solution(object):
    def cloneGraph(self, node):
        """
        :type node: Node
        :rtype: Node
        """
        if not node: return None
        map = dict()
        def copy(node):
          new = Node(node.val, [])
          map[node.val] = new

          for curr in node.neighbors:
            if not map.get(curr.val, False):
              ref = copy(curr)
              new.neighbors.append(ref)
            else:
              new.neighbors.append(map.get(curr.val))
          
          return new
          
        return copy(node)
