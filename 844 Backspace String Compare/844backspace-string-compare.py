class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        s_backspace_count = 0
        t_backspace_count = 0

        s_pointer = len(s) - 1
        t_pointer = len(t) - 1

        while s_pointer >= 0 or t_pointer >= 0:
            s_char = s[s_pointer] if s_pointer >= 0 else None
            t_char = t[t_pointer] if t_pointer >= 0 else None

            if s_char == '#':
                s_backspace_count += 1
                s_pointer -= 1
                continue

            if t_char == '#':
                t_backspace_count += 1
                t_pointer -= 1
                continue

            if s_backspace_count > 0:
                s_pointer -= 1
                s_backspace_count -= 1
                continue

            if t_backspace_count > 0:
                t_pointer -= 1
                t_backspace_count -= 1
                continue

            if s_char != t_char:
                return False

            s_pointer -= 1
            t_pointer -= 1

        return True
        