from math import inf

class Solution:
    def canAttendMeetings(self, intervals: list[list[int]]) -> bool:
        # that key can be omitted right
        intervals.sort(key=lambda interval: interval[0])

        for index, interval in enumerate(intervals):
            end = interval[1]
            next_start = intervals[index + 1][0] if index + 1 < len(intervals) else inf

            if end > next_start:
                return False

        return True            
        