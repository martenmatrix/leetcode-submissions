import heapq

class MedianFinder:

    def __init__(self):
        self.is_even = True

        self.min_heap = []
        self.max_heap = []
        

    def addNum(self, num: int) -> None:
        self.is_even = not self.is_even

        if not len(self.min_heap) or num >= self.min_heap[0]:
            heapq.heappush(self.min_heap, num)
        else:
            heapq.heappush_max(self.max_heap, num)
            
        # re-order if is even and the height differ
        if self.is_even and len(self.min_heap) != len(self.max_heap):
            if len(self.min_heap) > len(self.max_heap):
                curr = heapq.heappop(self.min_heap)
                heapq.heappush_max(self.max_heap, curr)
            else:
                curr = heapq.heappop_max(self.max_heap)
                heapq.heappush(self.min_heap, curr) 


    def findMedian(self) -> float:
        if self.is_even:
            num1 = self.min_heap[0]
            num2 = self.max_heap[0]

            return (num1 + num2) / 2

        return self.min_heap[0] if len(self.min_heap) >= len(self.max_heap) else self.max_heap[0]


# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()