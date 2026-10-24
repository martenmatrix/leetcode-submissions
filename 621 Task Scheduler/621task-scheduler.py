from collections import Counter, deque
import heapq

class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        task_count = Counter(tasks)

        max_heap = [-count for count in task_count.values()]
        heapq.heapify(max_heap)

        queue = deque()

        interval = 0

        while max_heap or queue:
            if max_heap:
                count = -heapq.heappop(max_heap)
                count -= 1

                if count > 0:
                    allowed_again_at = interval + n
                    queue.append((count, allowed_again_at))

            if queue and queue[0][1] <= interval:
                heapq.heappush(max_heap, -queue.popleft()[0])

            interval += 1

        return interval