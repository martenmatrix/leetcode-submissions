class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        if not len(nums):
            return [[]]

        sliced = nums[1:]

        smaller_permutations = self.permute(sliced)

        curr = nums[0]
        result = []

        for perm in smaller_permutations:
            for i in range(len(perm) + 1):
                copy = perm.copy()
                copy.insert(i, curr)
                result.append(copy)

        return result





        
        