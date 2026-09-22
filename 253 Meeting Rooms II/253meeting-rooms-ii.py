from math import inf

class Solution:
    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        intervals.sort(key=lambda interval: interval[0])
        heap = []
        count = 0

        for start, end in intervals:
            if heap and heap[0] <= start:
                heapq.heappop(heap)

            heapq.heappush(heap, end)
            count = max(count, len(heap))

        return count
