from collections import defaultdict
from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        conn = defaultdict(list)
        for course, prereq in prerequisites:
            conn[course].append(prereq)

        notCompl = set()
        compl = set()

        def dfs(course):
            if course in compl:
                return True
            deps = conn[course]
            if course in notCompl:
                return False

            notCompl.add(course)
            for dep in deps:
                if not dfs(dep):
                    return False

            notCompl.remove(course)
            compl.add(course)
            return True

        for course in range(numCourses):
            result = dfs(course)
            if not result:
                return False

        return True
