class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            middleIndex = math.floor((left + right) / 2)
            middleKey = nums[middleIndex]

            if middleKey == target:
                return middleIndex
            elif middleKey > target:
                right = middleIndex - 1
            else:
                left = middleIndex + 1

        return -1
