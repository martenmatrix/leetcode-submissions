class Solution:
    def maxArea(self, height: list[int]) -> int:
        def get_area(left, right):
            # lowest_bar times distance between them
            # Width counts gaps, not bars:
            # 8 — 6 — 2 — 5 — 4 — 8 — 3 — 7
            #   1   2   3   4   5   6   7
            # 6 bars between the walls, but 7 gaps.
            # Width = right - left = 8 - 1 = 7.
            return min(height[left], height[right]) * (right - left)

        curr_left = 0
        curr_right = len(height) - 1
        best_contain = get_area(curr_left, curr_right)

        while curr_left < curr_right:
            if height[curr_left] > height[curr_right]:
                curr_right -= 1
            else:
                # if smaller or equal does not matter
                curr_left += 1

            curr_contain = get_area(curr_left, curr_right)
            best_contain = max(best_contain, curr_contain)
            
        return best_contain