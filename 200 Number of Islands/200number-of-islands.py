class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        islands = 0

        def bfsMarker(x, y):
            grid[x][y] = "-1"
            directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

            for xmov, ymov in directions:
                newx = x + xmov
                newy = y + ymov

                if (
                    0 <= newx < len(grid)
                    and 0 <= newy < len(grid[0])
                    and grid[newx][newy] == "1"
                ):
                    bfsMarker(newx, newy)

        for rindex, row in enumerate(grid):
            for cindex, column in enumerate(row):
                if column == "1":
                    islands += 1
                    bfsMarker(rindex, cindex)

        return islands

        # idk if bfs or dfs matters here
        # for every row, for every column until first 1
        # for every 1, to a bfs, and mark every visited field with a -1 for visited
        # increase the counter by one and exit the loop
