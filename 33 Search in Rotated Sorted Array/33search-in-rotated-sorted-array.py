class Solution:
    def search(self, nums: list[int], target: int) -> int:
        # find the index where the start of the array is with binary search
        def findPivot(array):
            left = 0
            right = len(array) - 1

            while left != right:
                mid = (left + right) // 2

                if array[right] < array[mid]:
                    left = mid + 1
                else:
                    right = mid

            return left

        def binarySearch(l, r):
            while l != r:
                mid = (l + r) // 2

                if target > nums[mid]:
                    l = mid + 1
                else:
                    r = mid

            # does not matter if i return left or righ here, right
            return l if target == nums[l] else -1

        # smallest element at pivot
        pivot = findPivot(nums)
        smallest = nums[pivot]

        if smallest <= target <= nums[-1]:
            # Target could be in the sorted right portion.
            # Search from pivot through len(nums) - 1.
            return binarySearch(pivot, len(nums) - 1)
        elif smallest <= target <= nums[pivot - 1]:
            # Target could only be in the sorted left portion.
            # Search from 0 through pivot - 1.
            return binarySearch(0, pivot - 1)

        return -1
