from collections import deque


class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        queue = deque()
        result = 0
        fresh_oranges = 0

        for row_index, row in enumerate(grid):
            for column_index, cell in enumerate(row):
                if cell == 2:
                    queue.append((row_index, column_index, 0))
                elif cell == 1:
                    fresh_oranges += 1

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue:
            x, y, time = queue.popleft()
            time += 1

            for x_move, y_move in directions:
                new_x = x + x_move
                new_y = y + y_move

                if (
                    0 <= new_x < len(grid)
                    and 0 <= new_y < len(grid[0])
                    and grid[new_x][new_y] == 1
                ):
                    fresh_oranges -= 1
                    result = time
                    grid[new_x][new_y] = 2
                    queue.append((new_x, new_y, time))

        return result if not fresh_oranges else -1
