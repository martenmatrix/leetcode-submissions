class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        stack = []
        result = []

        for num in nums:
            stack.append((0, [num]))

        while len(stack):
            height, subresult = stack.pop()

            if height == len(nums) - 1:
                result.append(subresult)
                continue

            for num in nums:
                if num not in subresult:
                    stack.append((height + 1, subresult + [num]))

        return result
