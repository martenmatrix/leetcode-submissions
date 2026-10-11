class Solution:
    def romanToInt(self, s: str) -> int:
        count = 0
        
        values = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000,
        }

        for ichar in range(1, len(s)):
            prev = s[ichar - 1]
            curr = s[ichar]

            if prev == 'I' and (curr == 'V' or curr == 'X'):
                count -= 1
                continue
            elif prev == 'X' and (curr == 'L' or curr == 'C'):
                count -= 10
                continue
            elif prev == 'C' and (curr == 'D' or curr == 'M'):
                count -= 100
                continue
        
            count += values[prev]
        
        # there will be no special case for the last value, as nothing follows
        count += values[s[-1]]

        return count