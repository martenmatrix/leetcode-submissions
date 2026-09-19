class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        result = [0] * len(nums)

        prefix = 1
        for index in range(len(nums)):
          result[index] = prefix
          prefix *= nums[index]

        suffix = 1
        for index in range(len(nums) -1, -1, -1):
          result[index] *= suffix
          suffix *= nums[index]

        return result
