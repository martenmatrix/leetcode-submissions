from collections import defaultdict

class Solution:
    def findAnagrams(self, s: str, p: str) -> list[int]:
        if len(p) > len(s):
            return []

        s_count = defaultdict(int)
        p_count = defaultdict(int)
        res = []

        # create a initial solution, ask chatgpt if this would also work inline
        # e.g. this creates the sliding window which will then be changed in the loop
        for i in range(len(p)):
            s_count[s[i]] += 1
            p_count[p[i]] += 1

        # check if the first sliding windo is already a solution
        if s_count == p_count:
            res.append(0)

        # we start from last index of sliding window to delete its entry and because it was already checked above
        for i in range(len(p), len(s)):
            left = i - len(p)
            right = i
            old_char = s[left]
            new_char = s[right]

            # decrease
            s_count[old_char] -= 1

            if s_count[old_char] == 0:
                # if 0 we remove it so == comparison fails
                s_count.pop(old_char)
            
            s_count[new_char] += 1

            if s_count == p_count:
                res.append(left + 1)

        return res

        