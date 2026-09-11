from math import dist, inf
from typing import List
import heapq

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        maxheap = []

        for point in points:
            distance = dist((0, 0), point)
            biggest = -maxheap[0][0] if maxheap else inf

            if len(maxheap) < k:
                heapq.heappush(maxheap, (-distance, point))
            elif biggest > distance:
                heapq.heappop(maxheap)
                heapq.heappush(maxheap, (-distance, point))

        result = []
        for _, point in maxheap:
            result.append(point)

        return result
