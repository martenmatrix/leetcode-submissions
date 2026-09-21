class Solution:
    def combinationSum(self, nums, target):
        combinations = []
        # (currSum, includes, start)
        stack = [(0, [], 0)]

        while len(stack):
            currSum, includes, start = stack.pop()

            for i in range(start, len(nums)):
                nsum = currSum + nums[i]
                nincludes = [] + includes

                nincludes.append(nums[i])
                if nsum == target:
                    # if 0 at the end coulg be edge case
                    combinations.append(nincludes)
                elif nsum < target:
                    stack.append((nsum, nincludes, i))

        return combinations
