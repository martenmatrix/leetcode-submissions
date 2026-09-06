from math import inf
from typing import List

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # Check the edge case where intervals is empty.
        if not len(intervals):
            return [newInterval]

        # Insert the new interval in sorted start-time order.
        if newInterval[0] <= intervals[0][0]:
            intervals.insert(0, newInterval)
        else:
            for index, interval in enumerate(intervals):
                left = interval[0]
                right = intervals[index + 1][0] if index + 1 < len(intervals) else inf

                if left <= newInterval[0] <= right:
                    intervals.insert(index + 1, newInterval)
                    break

        result = []

        for interval in intervals:
            if not len(result):
                result.append(interval)
            else:
                last = result[-1]
                current = interval

                # Merge overlapping intervals.
                if current[0] <= last[1]:
                    result[-1][0] = min(last[0], current[0])
                    result[-1][1] = max(last[1], current[1])
                else:
                    result.append(interval)

        return result
