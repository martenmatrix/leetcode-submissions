class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        
        visited = set()

        def dfs(start, path):
            x, y = start

            if path == len(word):
                return True
            elif (not 0 <= x < len(board)
                  or 
                  not 0 <= y < len(board[0])
                  or
                  word[path] != board[x][y]
                  or
                  (x, y) in visited
                  ):
                return False

            visited.add((x, y))

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

            for dir in directions:
                new_x = x + dir[0]
                new_y = y + dir[1]

                res = dfs((new_x, new_y), path + 1)
                if res:
                    return True

            # clean up cell it added
            visited.remove((x, y))
            return False

        for row_i in range(len(board)):
            for col_i in range(len(board[0])):
                visited = set()
                found = dfs((row_i, col_i), 0)
                if found:
                    return True

        return False