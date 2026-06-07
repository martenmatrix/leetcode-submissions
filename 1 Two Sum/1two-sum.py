class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        numberAtIndex = {number: index for index, number in enumerate(nums)}

        for index, number in enumerate(nums):
            need = target - number

            if numberAtIndex.get(need, False):
                otherIndex = numberAtIndex.get(need)

                if index != otherIndex:
                    return [index, otherIndex]
