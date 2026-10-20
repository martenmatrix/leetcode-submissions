class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        prev_row = [1] * n
        # just has to have 1 at the end
        curr_row = [1] * n

        # dont need to go backwards, as it is just for the iterations
        for row_i in range(m - 1):
            for col_i in range(n - 2, -1, -1):
                curr_row[col_i] = prev_row[col_i] + curr_row[col_i + 1]
            
            prev_row = curr_row.copy()
            curr_row = [1] * n

        return prev_row[0]