class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        sums = set([0, nums[0]])

        for num in nums[1:]:
            for summ in sums.copy():
                sums.add(num + summ)
        
        return (total / 2) in sums