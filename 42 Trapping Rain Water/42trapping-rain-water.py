class Solution:
    def trap(self, height: list[int]) -> int:
        l, r = 0, len(height) - 1
        max_left, max_right = height[l], height[r]
        trapped_water = 0

        while l < r:
            new_trapped_water = 0

            if height[l] < height[r]:
                l += 1
                max_left = max(max_left, height[l])
                new_trapped_water += min(max_left, max_right) - height[l]
            else:
                r -= 1
                max_right = max(max_right, height[r])
                new_trapped_water += min(max_left, max_right) - height[r]

            if new_trapped_water > 0:
                trapped_water += new_trapped_water

        return trapped_water
