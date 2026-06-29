from collections import defaultdict

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        sCount = defaultdict(int)
        tCount = defaultdict(int)

        for char in s:
            sCount[char] += 1

        for char in t:
            tCount[char] += 1

        if len(sCount) != len(tCount):
            return False

        for key in sCount.keys():
            if sCount[key] != tCount[key]:
                return False

        return True

