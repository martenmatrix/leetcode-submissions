class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        if not len(matrix):
            return []

        visited = set([(0, 0)])
        # stack, can also be a queue, but stack is fine as we are just pushing one element at a time, can also just use one var instead of a stack
        stack = [(0, 0)]
        result = [matrix[0][0]]

        def try_append_to_result(next_x, next_y):
            next_elm = (next_x, next_y)
            exists = 0 <= (next_x) < len(matrix) and 0 <= (next_y) < len(matrix[next_x])
            if exists and next_elm not in visited:
                visited.add(next_elm)
                stack.append(next_elm)
                result.append(matrix[next_x][next_y])
                return True
            return False

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        curr_dir = 0

        while len(stack):
            x, y = stack.pop()

            for offset in range(4):
                direction_index = (curr_dir + offset) % 4
                next_x, next_y = directions[direction_index]

                inserted = try_append_to_result(x + next_x, y + next_y)
                if inserted:
                    # remember what direction succeeded and continue from there 
                    curr_dir = direction_index
                    break
                
        return result

        # 25 min for the code, will now do dry runs
        # time complexity i O(n * m), space complexity O(n * m) because of set or result array, both have the same space
        # 32 min after dry run and adjusting some cases as well as stating complexity, however still fails