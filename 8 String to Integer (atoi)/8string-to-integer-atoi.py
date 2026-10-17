class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.strip()
        count = 0
        allowed_map = {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
        }
        iteration = 0
        isNegative = False

        for i in range(len(s) - 1, -1, -1):
            char = s[i]

            if i == 0 and char in ["+", "-"]:
                if char == "-":
                    isNegative = True
                break

            if char not in allowed_map:
                count = 0
                iteration = 0
                continue;
            
            count += allowed_map[char] * 10 ** iteration

            iteration += 1

        if count >= (2 ** 31):
            count = (2 ** 31)

            if isNegative:
                return -count
            return count - 1

        if isNegative:
            return -count
        return count