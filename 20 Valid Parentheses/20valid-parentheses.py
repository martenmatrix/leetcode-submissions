class Solution:
    def isValid(self, s: str) -> bool:
        chars = list(s)
        stack = []

        for char in chars:
            topOfStack = stack[-1] if stack else None

            if char == ")" and topOfStack == "(":
                stack.pop()
            elif char == "]" and topOfStack == "[":
                stack.pop()
            elif char == "}" and topOfStack == "{":
                stack.pop()
            else:
                stack.append(char)

        if not stack:
            return True
        return False
