class TimeMap:
    def __init__(self):
        self.values = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        stored = self.values.get(key, None)

        if not stored:
            self.values[key] = [(value, timestamp)]
        else:
            self.values[key].append((value, timestamp))

        # our values will be sorted by timestamp, as this is guaranteed by a constraint that the set value is strictly increasing for the timestamp

    def get(self, key: str, timestamp: int) -> str:
        stored = self.values.get(key, None)

        if not stored:
            return ''

        if timestamp < stored[0][1]:
            return ""
        
        # binary search
        left = 0
        right = len(stored) - 1

        while left != right:
            curr = left + (right - left) // 2
            val, stored_timestamp = stored[curr]

            if timestamp > stored_timestamp:
                left = curr + 1

                if left < len(stored) and timestamp < stored[left][1]:
                    return val
            else:
                right = curr

        return stored[left][0]


# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)