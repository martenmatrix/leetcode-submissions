class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        result = []

        intervals.sort(key=lambda interval: interval[0])

        left, right = intervals[0]

        for index, (curr_left, curr_right) in enumerate(intervals):
            if right < curr_left:
                result.append([left, right])
                left = curr_left
                right = curr_right
            else:
                right = max(right, curr_right)
                left = min(left, curr_left)
        
        # last element can't reach first if condition, no matter, if they are overlapping or not
        result.append([left, right])

        return result