class Solution(object):
    def evalRPN(self, tokens):
        stack = []
        operators = ("+", "-", "*", "/")

        for token in tokens:
            if token in operators:
                right = int(stack.pop())
                left = int(stack.pop())

                if token == "+":
                    stack.append(left + right)
                elif token == "-":
                    stack.append(left - right)
                elif token == "*":
                    stack.append(left * right)
                elif token == "/":
                    stack.append(int(left / right))
            else:
                stack.append(token)

        return int(stack.pop())
