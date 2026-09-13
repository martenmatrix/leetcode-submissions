from collections import deque
from typing import List, Optional

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        queue = deque([root])
        result = []

        while len(queue):
            entry = []
            for i in range(len(queue)):
                elem = queue.popleft()
                if elem:
                    entry.append(elem.val)
                    queue.append(elem.left)
                    queue.append(elem.right)
            if entry:
                result.append(entry)

        return result
