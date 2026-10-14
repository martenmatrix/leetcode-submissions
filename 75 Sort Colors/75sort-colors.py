class Solution:
    def sortColors(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        
        l = 0
        r = len(nums) - 1
        i = 0

        def swap(a, b):
            temp = nums[a]
            nums[a] = nums[b]
            nums[b] = temp

        while i <= r:
            if nums[i] == 0:
                swap(l, i)
                l += 1
                i += 1
            elif nums[i] == 2:
                swap(r, i)
                r -= 1
            elif nums[i] == 1:
                i += 1
                