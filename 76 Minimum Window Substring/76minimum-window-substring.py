from collections import defaultdict
from math import inf

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        total_matches_required = len(t)
        required_chars = defaultdict(int)
        curr_chars = defaultdict(int)

        curr_total = 0
        shortest_length = inf

        for char in t:
            required_chars[char] += 1

        left = right = 0
        best_left = best_right = -1


        def covers_target():
            for char in required_chars:
                if curr_chars.get(char, 0) < required_chars.get(char, 0):
                    return False
            return True

        # we always execute the shrinking loop before revisitng this condition, and left < len would keep it in an indefinte loop as then the while loops below might never execute again
        while right < len(s):
            while not covers_target() and right < len(s):
                added_char = s[right]

                if added_char in required_chars:
                    curr_chars[added_char] += 1

                right += 1

            while covers_target() and left < len(s):
                char_to_remove = s[left]

                length = (right - left)

                if length < shortest_length:
                    shortest_length = length
                    best_left = left
                    best_right = right

                if char_to_remove in curr_chars:
                    curr_chars[char_to_remove] -= 1

                    if curr_chars[char_to_remove] == 0:
                        del curr_chars[char_to_remove]
                
                left += 1

        return s[best_left:best_right]