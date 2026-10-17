"""
# Definition for a Node.
class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next
"""

class Solution:
    def insert(self, head: 'Optional[Node]', insertVal: int) -> 'Node':
        if not head:
            # list is empty
            new = Node(insertVal)
            new.next = new
            return new

        curr = head.next
        prev = head

        def insert_between(left, right):
            left.next = Node(insertVal, right)
            return head
            
        while True:
            if prev.val <= insertVal <= curr.val:
                # normal insertion case, everybody thinks of
                return insert_between(prev, curr)
            elif prev.val > curr.val:
                # prev is the end, e.g prev is current biggest element and curr is smallest element
                # however there might still be elements, that haven't reached the correct gap, e.g. the other if checks, so carefully check this
                # only insert, if it would be the new maximum or minimum
                if insertVal > prev.val or insertVal < curr.val:
                    return insert_between(prev, curr)
            elif curr == head:
                # one full cycle, everything is the same, or just one node, just insert somewhere
                return insert_between(prev, curr)
        
            prev = curr
            curr = curr.next