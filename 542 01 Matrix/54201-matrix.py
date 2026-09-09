from collections import deque


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        queue = deque()

        for row_index, row in enumerate(mat):
            for column_index, cell in enumerate(row):
                if cell == 0:
                    queue.append((row_index, column_index, 0))
                else:
                    mat[row_index][column_index] = "#"

        while queue:
            row_index, column_index, distance = queue.popleft()
            steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]

            for row_step, column_step in steps:
                new_row = row_index + row_step
                new_column = column_index + column_step

                if (
                    not 0 <= new_row < len(mat)
                    or not 0 <= new_column < len(mat[0])
                    or mat[new_row][new_column] != "#"
                ):
                    continue

                new_distance = distance + 1
                mat[new_row][new_column] = new_distance
                queue.append((new_row, new_column, new_distance))

        return mat
