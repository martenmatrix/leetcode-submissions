class Solution:
    def calculate(self, s: str) -> int:
        # total before next parenthesis action
        total = 0
        # stores the current total number, important if we have more than two digits
        curr = 0
        # sign is positive at the start
        sign = 1
        stack = []

        for char in s:
            if char.isdigit():
                # e.g. weve built 1 and now also want to add 1, 1+1=2, which is wrong, therefore move the already save number 1 * 10 = 10 and add the value +1 = 11, which is correct for concatenating a string
                curr = curr * 10 + int(char)
            if char in "+-":
                # 2 + 2 - 2
                total += sign * curr
                curr = 0
                sign = 1 if char == "+" else -1
            if char == "(":
                # store curr total in stack
                stack.append(total)
                total = 0
                stack.append(sign)
                sign = 1
            if char == ")":
                # add the number curr stored in curr to the total
                total = total + sign * curr
                curr = 0

                sign = stack.pop()
                # only apply sign to total, as the element on the stack is already in the correct format and the sign only applies to the new number that comes outside of the parntheses
                total = total * sign + stack.pop()
                sign = 1

        # add last curr and sign, if nothing has to be added it will just add 0 and a positive +
        # one example where this is required would be just 2 + 2 but also (2 + 3) - 4
        return total + sign * curr