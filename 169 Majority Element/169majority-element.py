class Solution:
    def majorityElement(self, nums):
        numCount = defaultdict(int)
        requiredAppearance = floor(len(nums) / 2)
        for num in nums:
            numCount[num] += 1
            if numCount[num] > requiredAppearance:
                return num
