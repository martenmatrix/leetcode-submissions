from collections import defaultdict, deque

class Solution:
    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        if not edges:
            return [0]

        adj = defaultdict(list)
        adj_count = defaultdict(int)

        for src, dst in edges:
            adj[src].append(dst)
            adj[dst].append(src)
            adj_count[src] += 1
            adj_count[dst] += 1

        leafs_to_remove = deque()
        removed_count = 0

        for node, neighbor in adj.items():
            if len(neighbor) == 1:
                leafs_to_remove.append(node)

        while leafs_to_remove:
            if n - removed_count <= 2:
                return list(leafs_to_remove)


            for i in range(len(leafs_to_remove)):
                remove = leafs_to_remove.popleft()
                
                for neighbor in adj[remove]:
                    adj_count[neighbor] -= 1

                    if adj_count[neighbor] == 1:
                        leafs_to_remove.append(neighbor)

                removed_count += 1
