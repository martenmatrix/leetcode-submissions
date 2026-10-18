class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        result = [[]]

        for num in nums:
            for res in result.copy():
                new_res = res.copy()
                new_res.append(num)
                result.append(new_res)
        
        return result

        # time is O(n * 2^n) space is O(n * n^2)