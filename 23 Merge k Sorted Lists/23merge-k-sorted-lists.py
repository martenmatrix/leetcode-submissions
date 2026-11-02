# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        amount = len(lists)
        interval = 1 

        while interval < len(lists):
            # have to subtract interval, to make sure pointer at + interval exists
            for i in range(0, len(lists) - interval, interval * 2):
                lists[i] = self.mergeLists(lists[i], lists[i + interval])
            interval *= 2

        return lists[0] if lists else None

    def mergeLists(self, list1, list2):
        new_list = ListNode()
        # tail does not point forward
        tail = new_list
        while list1 and list2:
            # we always take the smallest and append, the lists are already sorted, so we can only move forward
            if list1.val <= list2.val:
                tail.next = list1
                tail = list1

                list1 = list1.next
            else:
                tail.next = list2
                tail = list2

                list2 = list2.next

        if list1:
            tail.next = list1
            tail = list1
        elif list2:
            tail.next = list2
            tail = list2

        return new_list.next if new_list.next else None
