class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}

        # dummy values
        # most recently used
        self.head = Node(-1, -1)
        # least recently used
        self.tail = Node(-1, -1)

        # otherwise accessing the indices crashes
        self.head.prev = self.tail
        self.tail.next = self.head

    def _remove(self, node):
        prev = node.prev
        next = node.next

        prev.next = next
        next.prev = prev  

    def _insert_as_most_recent(self, node):
        prev_most_recent = self.head.prev

        prev_most_recent.next = node
        node.prev = prev_most_recent

        node.next = self.head
        self.head.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        # its in the cache
        node = self.cache[key]
        self._remove(node)
        self._insert_as_most_recent(node)

        return node.val
        

    def put(self, key: int, value: int) -> None:
        new_node = Node(key, value)

        # still have to handle max exceeded
        
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
        else:
            node = Node(key, value)

        self.cache[key] = node
        self._insert_as_most_recent(node)

        # check if cache limit is too big
        if len(self.cache) > self.capacity:
            least_recent = self.tail.next

            # remove least used element from list
            self._remove(least_recent)
            # remove from cache
            del self.cache[least_recent.key]

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)