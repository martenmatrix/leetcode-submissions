class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        best = -inf
        # (index, height)
        stack = []

        for index, height in enumerate(heights):
            # earliest index where the rectangle of the current height can begin
            start = index

            while stack and stack[-1][1] > height:
                top_index, top_height = stack.pop()
                start = top_index

                # need to take the curr index, otherwise the first would be 0 and then we would do 0 times height
                best = max(best, (index - top_index) * top_height)

            stack.append((start, height))
        
        # e.g. no shorter bar ever arrived
        while stack:
            top_index, top_height = stack.pop()
            best = max(best, (len(heights) - top_index) * top_height)

        return best
