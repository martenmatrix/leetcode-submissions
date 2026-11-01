from bisect import bisect_left

class Solution:
    def jobScheduling(self, startTime: list[int], endTime: list[int], profit: list[int]) -> int:
        jobs = list(zip(startTime, endTime, profit))
        # sort jobs by start time
        jobs.sort()

        # otherwise tle
        memoization = [-1] * len(jobs)

        def dfs(i):
            # base condition
            if i == len(jobs):
                return 0

            if memoization[i] >= 0:
                return memoization[i]

            # skip it
            skip = dfs(i + 1)
            
            # take
            # get next possbile start index with binary search
            curr_end = jobs[i][1]
            next_i = bisect_left(jobs, curr_end, key=lambda job: job[0])
            profit = jobs[i][2]
            take = profit + dfs(next_i)

            best = max(skip, take)
            memoization[i] = best

            return best
            

        # dfs should return the best result
        return dfs(0)