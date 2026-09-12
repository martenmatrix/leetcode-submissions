from collections import defaultdict

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        charOccur = defaultdict(lambda: -1)
        bestLength = 0
        currLength = 0
        currStart = 0

        for index, char in enumerate(s):
            lastSeen = charOccur[char]
            charOccur[char] = index

            if lastSeen >= currStart:
                currStart = lastSeen + 1

            currLength = index - currStart + 1

            if currLength > bestLength:
                bestLength = currLength

        return bestLength
