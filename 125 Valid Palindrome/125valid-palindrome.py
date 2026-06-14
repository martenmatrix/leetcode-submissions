class Solution:
    def isPalindrome(self, s: str) -> bool:
        clean = "".join(character for character in s if character.isalnum()).lower()

        if len(clean) == 0:
            return True

        leftIndex = 0
        rightIndex = len(clean) - 1

        while True:
            if rightIndex < leftIndex:
                return True

            if leftIndex == rightIndex and clean[leftIndex] == clean[rightIndex]:
                return True

            if clean[leftIndex] != clean[rightIndex]:
                return False

            leftIndex += 1
            rightIndex -= 1
