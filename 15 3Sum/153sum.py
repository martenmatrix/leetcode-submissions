from collections import defaultdict

class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        complement = defaultdict(lambda: -1)

        for i, num in enumerate(nums):
            complement[num] = i

        result = set()
        # we only return values not indices, so if a value was already included here it cannot produce a new result
        processed = set()
        for i1, num1 in enumerate(nums):
            if num1 in processed:
                continue
            processed.add(num1)
            for i2, num2 in enumerate(nums):
                if i1 == i2:
                    continue

                need = -(num1 + num2)
                # .get() does not create entries for missing keys.
                has = complement.get(need, -1)

                if has != -1 and has != i1 and has != i2:
                    result.add(tuple(sorted((num1, num2, need))))

        return [list(triplet) for triplet in result]
