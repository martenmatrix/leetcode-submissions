from collections import defaultdict, deque

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:
        wordList.append(beginWord)
        word_adjacency = defaultdict(list)

        for word in wordList:
            for i in range(len(word)):
                matcher = word[:i] + "*" + word[i + 1:]
                word_adjacency[matcher].append(word)

        visited = set([beginWord])
        queue = deque([beginWord])
        iteration = 1 

        while queue:
            for _ in range(len(queue)):
                curr = queue.popleft()

                if curr == endWord:
                    return iteration

                for i in range(len(curr)):
                    matcher = curr[:i] + "*" + curr[i + 1:]
                    
                    for word in word_adjacency[matcher]:
                        if word not in visited:
                            visited.add(word)
                            queue.append(word)

            iteration += 1

        return 0
